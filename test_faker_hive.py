import unittest
import time
from mf_core import Hive


class TestHiveFaker(unittest.TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self.__hive = Hive()

    def test_generate_data(self):
        self.__hive.generate_data()
        self.assertGreater(self.__hive.last_temperature, 0.0)
        self.assertGreater(self.__hive.last_sound_level, 0.0)
        self.assertGreater(self.__hive.last_weight, 0.0)

    def test_generate_coherent_data(self):
        self.__hive.generate_data()
        temp1 = self.__hive.last_temperature
        self.assertGreaterEqual(self.__hive.last_temperature, 10.0)
        self.assertLessEqual(self.__hive.last_temperature, 45.0)
        weight1 = self.__hive.last_weight
        self.assertGreaterEqual(self.__hive.last_weight, 10000.0)
        self.assertLessEqual(self.__hive.last_weight, 100000.0)
        sound_level1 = self.__hive.last_sound_level
        self.assertGreaterEqual(self.__hive.last_sound_level, 35.0)
        self.assertLessEqual(self.__hive.last_sound_level, 75.0)
        self.__hive.generate_data()
        temp2 = self.__hive.last_temperature
        weight2 = self.__hive.last_weight
        sound_level2 = self.__hive.last_sound_level
        self.assertTrue(temp1 * 0.99 <= temp2 <= temp1 * 1.01)
        self.assertTrue(weight1 * 0.90 <= weight2 <= weight1 * 1.10)
        self.assertTrue(sound_level1 * 0.99 <= sound_level2 <= sound_level1 * 1.01)

    def test_generate_1_min(self):
        timestamp_now = int(time.time())
        timestamp_begin = timestamp_now - 60
        for i in range(0, 60, 5):
            self.__hive.generate_data(timestamp_begin + i)
        data = self.__hive.metrics_history.get_lines_between(timestamp_begin, timestamp_now)
        self.assertEqual(len(data), 12)

    def test_generate_24_hours(self):
        sec24h = 60 * 60 * 24
        timestamp_now = int(time.time())
        timestamp_begin = timestamp_now - sec24h
        for i in range(0, sec24h, 5):
            self.__hive.generate_data(timestamp_begin + i)
        data = self.__hive.metrics_history.get_lines_between(timestamp_begin, timestamp_now)
        self.assertEqual(len(data), (sec24h / 5))

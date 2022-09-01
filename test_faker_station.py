import unittest
import time
from mf_core import Station


# noinspection DuplicatedCode
class TestStationFaker(unittest.TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self.__station = Station()

    def test_generate_data(self):
        self.__station.generate_data()
        self.assertNotEqual(self.__station.last_temperature, 0.0)
        self.assertNotEqual(self.__station.last_sun, 0.0)
        self.assertNotEqual(self.__station.last_battery_state, 0.0)
        self.assertNotEqual(self.__station.last_rain, 0.0)
        self.assertNotEqual(self.__station.last_wind, 0.0)

    def test_generate_coherent_data(self):
        self.__station.generate_data()
        temp1 = self.__station.last_temperature
        sun1 = self.__station.last_sun
        battery_state1 = self.__station.last_battery_state
        rain1 = self.__station.last_rain
        wind1 = self.__station.last_wind
        self.__station.generate_data()
        temp2 = self.__station.last_temperature
        sun2 = self.__station.last_sun
        battery_state2 = self.__station.last_battery_state
        rain2 = self.__station.last_rain
        wind2 = self.__station.last_wind
        self.assertGreaterEqual(temp1, 0.0)
        self.assertLessEqual(temp1, 45.0)
        self.assertGreaterEqual(sun1, 0.0)
        self.assertLessEqual(sun1, 1.0)
        self.assertGreaterEqual(battery_state1, 0.01)
        self.assertLessEqual(battery_state1, 1.0)
        self.assertGreaterEqual(rain1, 0.0)
        self.assertLessEqual(rain1, 1000.0)
        self.assertGreaterEqual(wind1, 0.0)
        self.assertLessEqual(wind1, 50.0)
        self.assertTrue(temp1 * 0.99 <= temp2 <= temp1 * 1.01)
        self.assertTrue(sun1 - 0.02 <= sun2 <= sun1 + 0.02)
        self.assertTrue(battery_state1 - 0.02 <= battery_state2 <= battery_state1 + 0.02 and battery_state1 <= 1)
        self.assertTrue(rain2 >= rain1 or rain2 == 0.0)
        self.assertTrue(wind1 - 0.02 <= wind2 <= wind1 + 0.02)

    def test_generate_1_min(self):
        timestamp_now = int(time.time())
        timestamp_begin = timestamp_now - 60
        for i in range(0, 60, 5):
            self.__station.generate_data(timestamp_begin + i)
        data = self.__station.metrics_history.get_lines_between(timestamp_begin, timestamp_now)
        self.assertEqual(len(data), 12)

    def test_generate_24_hours(self):
        sec24h = 60 * 60 * 24
        timestamp_now = int(time.time())
        timestamp_begin = timestamp_now - sec24h
        for i in range(0, sec24h, 5):
            self.__station.generate_data(timestamp_begin + i)
        data = self.__station.metrics_history.get_lines_between(timestamp_begin, timestamp_now)
        self.assertEqual(len(data), (sec24h / 5))

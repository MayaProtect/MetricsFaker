import time
import unittest
from uuid import uuid4
from mf_core import Hive
from mf_core import MetricsHistory
from mf_core import MetricsHistoryLine


class TestMetricsFaker(unittest.TestCase):
    def test_instantiate_hive(self):
        hive = Hive()
        self.assertNotEqual(hive.uuid, None)
        self.assertEqual(hive.last_weight, 0.0)
        self.assertEqual(hive.last_sound_level, 0.0)
        self.assertEqual(hive.last_temperature, 0.0)

    def test_instantiate_hive_with_defined_uuid(self):
        uuid = uuid4()
        hive = Hive(uuid)
        self.assertEqual(hive.uuid, uuid)

    def test_insert_data(self):
        uuid = uuid4()
        hive = Hive(uuid)
        hive.insert_data(1.5, 2.0, 2.5)
        self.assertEqual(hive.uuid, uuid)
        self.assertEqual(hive.last_temperature, 1.5)
        self.assertEqual(hive.last_weight, 2.0)
        self.assertEqual(hive.last_sound_level, 2.5)

    def test_hive_metrics_history_return_type(self):
        hive = Hive()
        self.assertTrue(type(hive.metrics_history) == MetricsHistory)

    def test_hive_metrics_history_line_return_type(self):
        hive = Hive()
        hive.insert_data(1.0, 1.0, 1.0)
        self.assertTrue(type(hive.metrics_history[0]) == MetricsHistoryLine)

    def test_hive_metrics_history_obtain_data(self):
        hive = Hive()
        hive.insert_data(0.1, 0.2, 0.3)
        hive.insert_data(1.0, 2.0, 3.0)
        hive.insert_data(4.0, 5.0, 6.0)
        history = hive.metrics_history
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0].temperature, 0.0)
        self.assertEqual(history[0].weight, 0.0)
        self.assertEqual(history[0].sound_level, 0.0)
        self.assertEqual(str(history[0]), f"At {history[0].timestamp}: Temp=0.0°C, Weight=0.0g, SoundLevel=0.0db")
        self.assertEqual(history[1].temperature, 0.1)
        self.assertEqual(history[1].weight, 0.2)
        self.assertEqual(history[1].sound_level, 0.3)
        self.assertEqual(str(history[1]), f"At {history[1].timestamp}: Temp=0.1°C, Weight=0.2g, SoundLevel=0.3db")
        self.assertEqual(history[2].temperature, 1.0)
        self.assertEqual(history[2].weight, 2.0)
        self.assertEqual(history[2].sound_level, 3.0)
        self.assertEqual(str(history[2]), f"At {history[2].timestamp}: Temp=1.0°C, Weight=2.0g, SoundLevel=3.0db")
        self.assertEqual(hive.last_temperature, 4.0)
        self.assertEqual(hive.last_weight, 5.0)
        self.assertEqual(hive.last_sound_level, 6.0)

    def test_hive_metrics_history_get_lines_between(self):
        hive = Hive()
        timestamp_start = int(time.time())
        hive.insert_data(1.0, 1.0, 1.0)
        hive.insert_data(1.0, 1.0, 1.0)
        hive.insert_data(1.0, 1.0, 1.0)
        self.assertEqual(len(hive.metrics_history.get_lines_between(timestamp_start)), 3)
        time.sleep(3)
        hive.insert_data(1.0, 1.0, 1.0)
        hive.insert_data(1.0, 1.0, 1.0)
        hive.insert_data(1.0, 1.0, 1.0)
        hive.insert_data(1.0, 1.0, 1.0)
        hive.insert_data(1.0, 1.0, 1.0)
        hive.insert_data(1.0, 1.0, 1.0)
        self.assertEqual(len(hive.metrics_history.get_lines_between(timestamp_start + 2)), 6)
        timestamp_end = int(time.time())
        time.sleep(2)
        hive.insert_data(1.0, 1.0, 1.0)
        hive.insert_data(1.0, 1.0, 1.0)
        hive.insert_data(1.0, 1.0, 1.0)
        self.assertEqual(len(hive.metrics_history.get_lines_between(timestamp_start + 2, timestamp_end)), 6)
        self.assertEqual(len(hive.metrics_history.get_lines_between(timestamp_start)), 12)

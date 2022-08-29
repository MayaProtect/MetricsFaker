import time
import unittest
from uuid import uuid4, UUID
from mf_core import Hive
from mf_core import MetricsHistory
from mf_core import HiveMetricsHistoryLine
from mf_core import StationMetricsHistoryLine
from mf_core import Station
from mf_core import HiveCollection


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

    def test_hive_insert_data(self):
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
        self.assertTrue(type(hive.metrics_history[0]) == HiveMetricsHistoryLine)

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

    def test_instantiate_station(self):
        station = Station()
        self.assertNotEqual(station.uuid, None)
        self.assertEqual(station.last_temperature, 0.0)
        self.assertEqual(station.last_sun, 0.0)
        self.assertEqual(station.last_battery_state, 0.0)
        self.assertEqual(station.last_wind, 0.0)
        self.assertEqual(station.last_rain, 0.0)

    def test_instantiate_station_with_uuid(self):
        uuid = uuid4()
        station = Station(uuid)
        self.assertEqual(station.uuid, uuid)

    def test_station_insert_data(self):
        station = Station()
        station.insert_data(1.0, 2.0, 3.0, 4.0, 5.0)
        self.assertEqual(station.last_temperature, 1.0)
        self.assertEqual(station.last_sun, 2.0)
        self.assertEqual(station.last_battery_state, 3.0)
        self.assertEqual(station.last_wind, 4.0)
        self.assertEqual(station.last_rain, 5.0)

    def test_station_history_return_type(self):
        station = Station()
        self.assertTrue(type(station.metrics_history) == MetricsHistory)

    def test_station_metrics_history_line_return_type(self):
        station = Station()
        station.insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        self.assertTrue(type(station.metrics_history[0]) == StationMetricsHistoryLine)

    def test_station_metrics_history_obtain_data(self):
        station = Station()
        station.insert_data(0.1, 0.2, 0.3, 0.4, 0.5)
        station.insert_data(1.0, 2.0, 3.0, 4.0, 5.0)
        station.insert_data(4.0, 5.0, 6.0, 7.0, 8.0)
        history = station.metrics_history
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0].temperature, 0.0)
        self.assertEqual(history[0].sun, 0.0)
        self.assertEqual(history[0].battery_state, 0.0)
        self.assertEqual(history[0].wind, 0.0)
        self.assertEqual(history[0].rain, 0.0)
        self.assertEqual(str(history[0]), f"At {history[0].timestamp}: Temp=0.0°C, Sun=0.0%, Battery=0.0%, Wind=0.0m/s, Rain=0.0mm")
        self.assertEqual(history[1].temperature, 0.1)
        self.assertEqual(history[1].sun, 0.2)
        self.assertEqual(history[1].battery_state, 0.3)
        self.assertEqual(history[1].wind, 0.4)
        self.assertEqual(history[1].rain, 0.5)
        self.assertEqual(str(history[1]), f"At {history[1].timestamp}: Temp=0.1°C, Sun=0.2%, Battery=0.3%, Wind=0.4m/s, Rain=0.5mm")
        self.assertEqual(history[2].temperature, 1.0)
        self.assertEqual(history[2].sun, 2.0)
        self.assertEqual(history[2].battery_state, 3.0)
        self.assertEqual(history[2].wind, 4.0)
        self.assertEqual(history[2].rain, 5.0)
        self.assertEqual(str(history[2]), f"At {history[2].timestamp}: Temp=1.0°C, Sun=2.0%, Battery=3.0%, Wind=4.0m/s, Rain=5.0mm")
        self.assertEqual(station.last_temperature, 4.0)
        self.assertEqual(station.last_sun, 5.0)
        self.assertEqual(station.last_battery_state, 6.0)
        self.assertEqual(station.last_wind, 7.0)
        self.assertEqual(station.last_rain, 8.0)

    def test_station_metrics_history_get_lines_between(self):
        station = Station()
        timestamp_start = int(time.time())
        station.insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        station.insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        station.insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        self.assertEqual(len(station.metrics_history.get_lines_between(timestamp_start)), 3)
        time.sleep(3)
        station.insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        station.insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        station.insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        station.insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        station.insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        station.insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        self.assertEqual(len(station.metrics_history.get_lines_between(timestamp_start + 2)), 6)
        timestamp_end = int(time.time())
        time.sleep(2)
        station.insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        station.insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        station.insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        self.assertEqual(len(station.metrics_history.get_lines_between(timestamp_start + 2, timestamp_end)), 6)
        self.assertEqual(len(station.metrics_history.get_lines_between(timestamp_start)), 12)

    def test_station_create_hive(self):
        station = Station()
        station.hive_collection.create_hive()
        station.hive_collection.create_hive()
        uuid = station.hive_collection.create_hive()
        self.assertTrue(type(uuid) == UUID)
        self.assertTrue(len(station.hive_collection), 3)

    def test_hive_collection_collect_data(self):
        timestamp_start = int(time.time())
        hc = HiveCollection()
        uuid = hc.create_hive()
        hc[0].insert_data(1.0, 1.0, 1.0)
        hc[0].insert_data(1.0, 1.0, 1.0)
        time.sleep(1)
        data = hc.collect_data()
        self.assertTrue(type(data) == list)
        self.assertEqual(len(data), 2)
        self.assertEqual(str(data[1]["hive_id"]), str(uuid))
        timestamp_end = int(time.time())
        self.assertEqual(len(data[0]), 5)
        self.assertTrue(timestamp_start <= data[0]["timestamp"] <= timestamp_end)
        self.assertEqual(data[1]["temperature"], 1.0)
        self.assertEqual(data[1]["weight"], 1.0)
        self.assertEqual(data[1]["sound_level"], 1.0)
        time.sleep(5)
        hc[0].insert_data(1.0, 1.0, 1.0)
        hc[0].insert_data(1.0, 1.0, 1.0)
        hc[0].insert_data(1.0, 1.0, 1.0)
        hc[0].insert_data(1.0, 1.0, 1.0)
        data = hc.collect_data()
        self.assertEqual(len(data), 4)

    def test_station_collection_create_station(self):
        pass

    def test_station_collection_collect_data(self):
        pass

    def test_station_collection_collect_hives_data(self):
        pass

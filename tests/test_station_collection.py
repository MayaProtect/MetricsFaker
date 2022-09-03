import unittest
import time
from uuid import UUID

from mf_core import StationCollection, Station


class TestStationCollection(unittest.TestCase):
    def test_create_station(self):
        sc = StationCollection()
        sc.create_station()
        self.assertTrue(type(sc[0]) == Station)

    def test_station_collection_create_station(self):
        sc = StationCollection()
        uuid = sc.create_station()
        self.assertTrue(type(uuid) == UUID)
        self.assertTrue(str(sc[0].uuid) == str(uuid))
        sc.create_station()
        sc.create_station()
        self.assertEqual(len(sc), 3)

    def test_return_coherent_uuid(self):
        sc = StationCollection()
        uuid = sc.create_station()
        self.assertTrue(uuid == sc[0].uuid)

    def test_get_by_uuid(self):
        sc = StationCollection()
        uuid = sc.create_station()
        station = sc.get_by_uuid(uuid)
        self.assertTrue(station == sc[0])

    def test_station_collection_collect_data(self):
        timestamp_start = int(time.time())
        sc = StationCollection()
        uuid = sc.create_station()
        sc[0].insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        sc[0].insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        time.sleep(1)
        data = sc.collect_data()
        self.assertEqual(len(data), 2)
        self.assertEqual(len(data[0]), 7)
        self.assertEqual(str(data[0]["station_id"]), str(uuid))
        timestamp_end = int(time.time())
        self.assertTrue(timestamp_start <= data[0]["timestamp"] <= timestamp_end)
        self.assertTrue(type(data[0]["timestamp"]) == int)
        self.assertEqual(data[1]["temperature"], 1.0)
        self.assertEqual(data[1]["sun"], 1.0)
        self.assertEqual(data[1]["rain"], 1.0)
        self.assertEqual(data[1]["wind"], 1.0)
        self.assertEqual(data[1]["battery_state"], 1.0)
        time.sleep(5)
        sc[0].insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        sc[0].insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        sc[0].insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        sc[0].insert_data(1.0, 1.0, 1.0, 1.0, 1.0)
        data = sc.collect_data()
        self.assertEqual(len(data), 4)

    def test_station_collection_collect_hives_data(self):
        sc = StationCollection()
        for i in range(5):
            sc.create_station()
            for j in range(5):
                sc[i].hive_collection.create_hive()
                sc[i].hive_collection[j].insert_data(1.0, 1.0, 1.0)
        data = sc.collect_hives_data()
        self.assertEqual(len(data), 25)

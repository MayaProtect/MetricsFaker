import unittest
import time

from mf_core import HiveCollection, Hive


class TestHiveCollection(unittest.TestCase):
    def test_create_hive(self):
        hc = HiveCollection()
        hc.create_hive()
        self.assertTrue(type(hc[0]) == Hive)

    def test_return_coherent_uuid(self):
        hc = HiveCollection()
        uuid = hc.create_hive()
        self.assertTrue(uuid == hc[0].uuid)

    def test_get_by_uuid(self):
        hc = HiveCollection()
        uuid = hc.create_hive()
        hive = hc.get_by_uuid(uuid)
        self.assertTrue(hive == hc[0])

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
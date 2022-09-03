import unittest
import time
from mf_core import HiveEventCollection, HiveEvent


class TestHiveEventCollection(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.__hive_event_collection = HiveEventCollection()

    def test_create_event(self):
        self.__hive_event_collection.create_event("test", int(time.time()), "test")
        self.assertTrue(type(self.__hive_event_collection[0]) == HiveEvent)

    def test_return_coherent_uuid(self):
        uuid = self.__hive_event_collection.create_event("test", int(time.time()), "test")
        self.assertTrue(uuid == self.__hive_event_collection[0].uuid)

    def test_get_by_uuid(self):
        uuid = self.__hive_event_collection.create_event("test", int(time.time()), "test")
        hive_event = self.__hive_event_collection.get_by_uuid(uuid)
        self.assertTrue(hive_event == self.__hive_event_collection[0])

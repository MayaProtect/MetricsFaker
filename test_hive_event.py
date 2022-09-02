import unittest
from mf_core import HiveEvent


class TestHiveEvent(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.__hive_event = HiveEvent("test", 0, "test")

    def test_create_event(self):
        self.assertTrue(type(self.__hive_event) == HiveEvent)

    def test_return_coherent_uuid(self):
        self.assertTrue(self.__hive_event.uuid == self.__hive_event.uuid)

    def test_get_by_uuid(self):
        self.assertTrue(self.__hive_event == self.__hive_event)

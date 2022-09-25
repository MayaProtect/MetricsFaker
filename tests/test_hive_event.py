import unittest
from mf_core import HiveEvent
from uuid import UUID


class TestHiveEvent(unittest.TestCase):
    def __init__(self, method_name: str = ...) -> None:
        super().__init__(method_name)
        self.__hive_event = HiveEvent("test", 0, "test")

    def test_create_event(self):
        self.assertTrue(type(self.__hive_event) is HiveEvent)

    def test_return_coherent_uuid(self):
        self.assertTrue(type(self.__hive_event.uuid) is UUID)

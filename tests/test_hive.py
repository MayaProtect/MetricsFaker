import unittest
from mf_core import Hive, HiveEventCollection, Owner
from uuid import UUID, uuid4


class TestHive(unittest.TestCase):
    def __init__(self, method_name: str = ...) -> None:
        super().__init__(method_name)
        self.__hive = Hive()

    def test_create_hive(self):
        self.assertTrue(type(self.__hive) == Hive)
        self.assertEqual(self.__hive.last_weight, 0.0)
        self.assertEqual(self.__hive.last_sound_level, 0.0)
        self.assertEqual(self.__hive.last_temperature, 0.0)

    def test_return_coherent_uuid(self):
        self.assertTrue(type(self.__hive.uuid) is UUID)

    def test_create_hive_with_specified_uuid(self):
        uuid = uuid4()
        hive = Hive(uuid)
        self.assertTrue(hive.uuid == uuid)

    def test_hive_insert_data(self):
        self.__hive.insert_data(1.0, 2.0, 3.0)
        self.assertEqual(self.__hive.last_temperature, 1.0)
        self.assertEqual(self.__hive.last_weight, 2.0)
        self.assertEqual(self.__hive.last_sound_level, 3.0)

    def test_hive_events_return_type(self):
        self.assertTrue(type(self.__hive.events) == HiveEventCollection)

    def test_hive_add_event(self):
        self.__hive.add_event("test", "test", 0)
        self.assertEqual(len(self.__hive.events), 1)

    def test_set_owner(self):
        owner = Owner()
        self.__hive.owner = owner
        self.assertEqual(self.__hive.__owner, owner)
        
    def test_get_owner(self):
        owner = Owner()
        self.__hive.__owner = owner
        self.assertEqual(self.__hive.owner, owner)

    def test_get_owner_uuid(self):
        owner = Owner()
        self.__hive.owner = owner
        self.assertTrue(self.__hive.owner.uuid == owner.uuid)

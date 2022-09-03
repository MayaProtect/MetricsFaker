import unittest
from mf_core import Station, Owner
from uuid import uuid4, UUID


class TestStation(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.__station = Station()

    def test_create_station(self):
        self.assertTrue(type(self.__station) == Station)
        self.assertNotEqual(self.__station.uuid, None)
        self.assertEqual(self.__station.last_temperature, 0.0)
        self.assertEqual(self.__station.last_sun, 0.0)
        self.assertEqual(self.__station.last_battery_state, 0.0)
        self.assertEqual(self.__station.last_wind, 0.0)
        self.assertEqual(self.__station.last_rain, 0.0)

    def test_create_station_with_specified_uuid(self):
        uuid = uuid4()
        station = Station(uuid)
        self.assertTrue(station.uuid == uuid)

    def test_station_insert_data(self):
        self.__station.insert_data(1.0, 2.0, 3.0, 4.0, 5.0)
        self.assertEqual(self.__station.last_temperature, 1.0)
        self.assertEqual(self.__station.last_sun, 2.0)
        self.assertEqual(self.__station.last_battery_state, 3.0)
        self.assertEqual(self.__station.last_wind, 4.0)
        self.assertEqual(self.__station.last_rain, 5.0)

    def test_station_set_owner(self):
        owner = Owner()
        self.__station.owner = owner
        self.assertTrue(self.__station.owner == owner)

    def test_station_get_owner(self):
        owner = Owner()
        self.__station.owner = owner
        self.assertTrue(self.__station.owner == owner)

    def test_station_get_owner_uuid(self):
        uuid = uuid4()
        owner = Owner(uuid)
        self.__station.owner = owner
        self.assertTrue(self.__station.owner.uuid == uuid)

    def test_station_create_hive(self):
        station = Station()
        station.hive_collection.create_hive()
        station.hive_collection.create_hive()
        uuid = station.hive_collection.create_hive()
        self.assertTrue(type(uuid) == UUID)
        self.assertTrue(len(station.hive_collection), 3)

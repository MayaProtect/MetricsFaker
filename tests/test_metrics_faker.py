import unittest
from app import MetricsFaker


class TestMetricsFaker(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

        self.__mongo_params = {
            "host": 'mongodb',
            "port": 8090,
        }

        self.__opentsdb_params = {
            "host": 'opentsdb',
            "port": 8091,
        }

        self.__faker_params = {
            "min_owner": 10,
            "max_owner": 25,
            "min_stations_per_owner": 2,
            "max_stations_per_owner": 5,
            "min_hives_per_station": 8,
            "max_hives_per_station": 25,
        }

        self.__metrics_faker = MetricsFaker(self.__mongo_params, self.__opentsdb_params, self.__faker_params)

    def test_create_metrics_faker(self):
        self.assertTrue(type(self.__metrics_faker) == MetricsFaker)

    def test_run(self):
        nbr_hive = 0
        self.__metrics_faker.run()
        self.assertTrue(self.__faker_params['min_owner'] <=
                        len(self.__metrics_faker.owner_collection) <=
                        self.__faker_params['max_owner'])

        self.assertTrue((self.__faker_params['min_stations_per_owner'] * len(self.__metrics_faker.owner_collection)) <=
                        len(self.__metrics_faker.station_collection) <=
                        self.__faker_params['max_stations_per_owner'] * len(self.__metrics_faker.owner_collection))

        for station in self.__metrics_faker.station_collection:
            self.assertTrue(self.__faker_params['min_hives_per_station'] <=
                            len(station.hive_collection) <=
                            self.__faker_params['max_hives_per_station'])
            nbr_hive += len(station.hive_collection)

        min_hives = self.__faker_params['min_hives_per_station'] * len(self.__metrics_faker.station_collection)
        max_hives = self.__faker_params['max_hives_per_station'] * len(self.__metrics_faker.station_collection)
        self.assertTrue(min_hives <= nbr_hive <= max_hives)

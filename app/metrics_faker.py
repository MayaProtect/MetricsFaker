import multiprocessing

from mf_core import StationCollection, Owner
from random import randint


class MetricsFaker:
    def __init__(self, mongo_params: dict, opentsdb_params: dict, faker_params: dict):
        """
        Create new instance of MetricsFaker App

        :param mongo_params: dict with mongo host and port :param opentsdb_params: dict with opentsdb host and port
        :param faker_params: dict with min_owner, max_owner, min_stations_per_owner, max_stations_per_owner,
        min_hives_per_station, max_hives_per_station
        """
        self.__mongo_params = mongo_params
        self.__opentsdb_params = opentsdb_params
        self.__faker_params = faker_params

        self.__station_collection = StationCollection()
        self.__owner_collection = []

        self.__cpu_count = multiprocessing.cpu_count()
        self.__max_process_per_core = 2
        self.__active_process = 0

    @property
    def owner_collection(self):
        return self.__owner_collection

    @property
    def station_collection(self):
        return self.__station_collection

    def run(self) -> None:
        """
        Run MetricsFaker App
        """
        self.__create_owners()
        self.__create_stations()
        self.__create_hives()

    def stop(self) -> None:
        """
        Stop MetricsFaker App
        """
        pass

    def __create_owners(self) -> None:
        """
        Create owners
        """
        for i in range(randint(self.__faker_params['min_owner'], self.__faker_params['max_owner'])):
            self.__owner_collection.append(Owner.generate_fake())

    def __create_stations(self) -> None:
        """
        Create stations
        """
        for i in range(len(self.__owner_collection)):
            for j in range(randint(self.__faker_params['min_stations_per_owner'],
                                   self.__faker_params['max_stations_per_owner'])):
                self.__station_collection.generate_fake(self.__owner_collection[i])

    def __create_hives(self) -> None:
        """
        Create hives
        """
        for i in range(len(self.__station_collection)):
            for j in range(randint(self.__faker_params['min_hives_per_station'],
                                   self.__faker_params['max_hives_per_station'])):
                self.__station_collection[i].generate_fake_hive()

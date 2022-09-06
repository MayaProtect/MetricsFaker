import multiprocessing
import logging
import threading
import time

from pymongo import MongoClient

from mf_core import StationCollection, Owner
from app.queued_item import QueuedItem
from app.worker import Worker
from random import randint
from uuid import uuid4


class MetricsFaker(threading.Thread):
    def __init__(self, mongo_params: dict, opentsdb_params: dict, faker_params: dict, start_timestamp: int = 0):
        """
        Create new instance of MetricsFaker App

        :param mongo_params: dict with mongo host and port :param opentsdb_params: dict with opentsdb host and port
        :param faker_params: dict with min_owner, max_owner, min_stations_per_owner, max_stations_per_owner,
        min_hives_per_station, max_hives_per_station
        """
        super(MetricsFaker, self).__init__()
        self.__mongo_params = mongo_params
        self.__opentsdb_params = opentsdb_params
        self.__faker_params = faker_params
        self.__start_timestamp = start_timestamp if start_timestamp > 0 else int(time.time())

        self.__station_collection = StationCollection()
        self.__owner_collection = []

        self.__cpu_count = multiprocessing.cpu_count()
        self.__max_process_per_core = 5
        self.__active_process = 0
        self.__worker_pool = []

        self.__logger = logging.getLogger('MetricsFaker')
        self.__logger.setLevel(logging.INFO)
        self.__logger.addHandler(logging.StreamHandler())
        self.__logger.addHandler(logging.FileHandler('metrics_faker.log'))
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.__logger.handlers[0].setFormatter(formatter)
        self.__logger.handlers[1].setFormatter(formatter)

        self.__logger.info("MetricsFaker App launched")

        self.__mongo_client = MongoClient(self.__mongo_params['host'], self.__mongo_params['port'], uuidRepresentation='standard')
        self.__mongo_db = self.__mongo_client['mayaprotect']

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

        self.__logger.info("MetricsFaker App started")
        if self.__start_timestamp < int(time.time()):
            self.__logger.info("Starting from {0}".format(self.__start_timestamp))

            timestamps = self.__calc_timestamp()
            self.__logger.info("Processing {0} timestamps".format(len(timestamps)))

            # TODO Create QueuedItems for each timestamp
            queued_items = self.__create_queued_items(timestamps)
            self.__logger.info("Processing {0} queued items".format(len(queued_items)))

            # TODO Create Workers
            nbr_workers = self.__cpu_count * self.__max_process_per_core
            nbr_items_per_worker = int(len(queued_items) / nbr_workers)
            self.__logger.info("Creating {0} workers".format(nbr_workers))
            for i in range(nbr_workers):
                worker = Worker(self.__logger, str(uuid4()))
                self.__worker_pool.append(worker)
                try:
                    for j in range(nbr_items_per_worker):
                        worker.add(queued_items.pop(0))
                except IndexError:
                    pass

            # TODO Start Workers
            for i in range(nbr_workers):
                self.__worker_pool[i].start()

    def __create_queued_items(self, timestamps: list) -> list:
        queued_items = []
        for timestamp in timestamps:
            for i in range(len(self.__station_collection)):
                queued_item = QueuedItem(self.__station_collection[i], timestamp)
                queued_items.append(queued_item)
        return queued_items

    def __calc_timestamp(self) -> list:
        timestamps = []
        for i in range(self.__start_timestamp, int(time.time()), 5):
            timestamps.append(i)
        return timestamps

    def stop(self) -> None:
        """
        Stop MetricsFaker App
        """
        pass

    def __create_owners(self) -> None:
        """
        Create owners
        """
        coll = self.__mongo_db['owners']
        for i in range(randint(self.__faker_params['min_owner'], self.__faker_params['max_owner'])):
            owner = Owner.generate_fake()
            self.__owner_collection.append(owner)
            coll.insert_one(owner.to_dict())

        self.__logger.info("{0} Owners created".format(len(self.__owner_collection)))

    def __create_stations(self) -> None:
        """
        Create stations
        """
        coll = self.__mongo_db['stations']
        for i in range(len(self.__owner_collection)):
            for j in range(randint(self.__faker_params['min_stations_per_owner'],
                                   self.__faker_params['max_stations_per_owner'])):
                self.__station_collection.generate_fake(self.__owner_collection[i])
                coll.insert_one(self.__station_collection[j].to_dict())

        self.__logger.info("{0} Stations created".format(len(self.__station_collection)))

    def __create_hives(self) -> None:
        """
        Create hives
        """
        coll_hives = self.__mongo_db['hives']
        coll_stations = self.__mongo_db['stations']
        coll_owners = self.__mongo_db['owners']

        nbr_hives_created = 0
        for station in self.__station_collection:
            for j in range(randint(self.__faker_params['min_hives_per_station'],
                                   self.__faker_params['max_hives_per_station'])):
                station.generate_fake_hive()
                nbr_hives_created += 1
                coll_hives.insert_one(station.hive_collection[j].to_dict())
                coll_hives.update_one({'uuid': station.hive_collection[j].uuid}, {'$set': {'station_uuid': station.uuid}})
                coll_stations.update_one({'uuid': station.uuid}, {'$push': {'hives': station.hive_collection[j].uuid}})
                coll_owners.update_one({'uuid': station.owner.uuid}, {'$push': {'hives': station.hive_collection[j].uuid}})

        self.__logger.info("{0} Hives created".format(nbr_hives_created))

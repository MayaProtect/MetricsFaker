import multiprocessing
import logging
import threading
import time
import math

from pymongo import MongoClient

from mf_core import StationCollection, Owner
from app.worker import Worker
from app.metrics_exporter import MetricsExporter
from random import randint
from uuid import uuid4


class MetricsFaker(threading.Thread):
    def __init__(self, mongo_params: dict, faker_params: dict, start_timestamp: int = 0):
        """
        Create new instance of MetricsFaker App

        :param mongo_params: dict with mongo host and port
        :param faker_params: dict with min_owner, max_owner, min_stations_per_owner, max_stations_per_owner,
        min_hives_per_station, max_hives_per_station
        """
        super(MetricsFaker, self).__init__()
        self.__mongo_params = mongo_params
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

        self.__mongo_client = MongoClient(self.__mongo_params['host'], int(self.__mongo_params['port']), uuidRepresentation='standard')
        self.__mongo_db = self.__mongo_client[self.__mongo_params['db']]

        self.__metrics_exporter = None

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

        self.__metrics_exporter = MetricsExporter(self.__station_collection, self.__logger, self.__faker_params['exporter_port'])
        self.__metrics_exporter.start()

        self.__logger.info("MetricsFaker App started")

        nbr_workers = self.__cpu_count * self.__max_process_per_core
        self.__logger.info("Creating {0} workers".format(nbr_workers))
        nbr_items_per_worker = math.ceil(len(self.__station_collection) / nbr_workers)
        needed_worker = int(len(self.__station_collection) / nbr_items_per_worker)
        if needed_worker < nbr_workers:
            nbr_workers = needed_worker
        for i in range(nbr_workers):
            worker = Worker(self.__logger, str(uuid4()))
            self.__worker_pool.append(worker)
            try:
                for j in range(nbr_items_per_worker):
                    worker.add_station(self.__station_collection[i * nbr_items_per_worker + j])
            except IndexError:
                pass
            worker.start()

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

import threading
import time

from mf_core import Station
import logging


class Worker(threading.Thread):
    def __init__(self, logger: logging.Logger, name: str = "Worker"):
        super(Worker, self).__init__()
        self.__name = name
        self.__stations = []
        self.__logger = logger
        self.__logger.info("Worker {0} created".format(name))

    @property
    def name(self):
        return self.__name

    @property
    def stations(self):
        return self.__stations

    def add_station(self, station: Station):
        self.__stations.append(station)
        self.__logger.info("Worker {0} added station {1}".format(self.__name, station.uuid))

    def run(self):
        while True:
            start_time = time.time()
            for station in self.__stations:
                station.generate_data()
                self.__logger.info("Worker {0} generated data for station {1}".format(self.__name, station.uuid))

                for hive in station.hive_collection:
                    hive.generate_data()
                    self.__logger.info("Worker {0} generated data for hive {1}".format(self.__name, hive.uuid))

            time.sleep(5 - (time.time() - start_time))

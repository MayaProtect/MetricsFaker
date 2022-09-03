import threading
from app.queued_item import QueuedItem
import logging


class Worker(threading.Thread):
    def __init__(self, logger: logging.Logger, name: str = "Worker"):
        super(Worker, self).__init__()
        self.__name = name
        self.__queue = []
        self.__logger = logger
        self.__logger.info("Worker {0} created".format(name))

    @property
    def queue(self):
        return self.__queue

    @property
    def name(self):
        return self.__name

    def run(self):
        while len(self.__queue) > 0:
            item = self.__queue.pop(0)
            self.__logger.info("Worker {0} processed {1}".format(self.name, item.station.uuid))
            item.station.generate_data(item.timestamp)
            for hive in item.station.hive_collection:
                hive.generate_data(item.timestamp)
                self.__logger.info("Worker {0} processed {1} from station {2}".format(self.name,
                                                                                      hive.uuid,
                                                                                      item.station.uuid))
            self.__logger.info("Worker {0} finished {1}".format(self.name, item.station.uuid))
            data_hives = item.station.hive_collection.collect_data()
            self.__logger.info("Worker {0} has {1} items remaining in queue".format(self.name, len(self.__queue)))

        self.__logger.info("Worker {0} finished".format(self.name))

    def add(self, item: QueuedItem):
        self.__logger.debug("Worker {0} added station {1} for timestamp {2}".format(self.name,
                                                                                    item.station.uuid,
                                                                                    item.timestamp))
        self.__queue.append(item)

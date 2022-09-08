import threading
from app.queued_item import QueuedItem
import logging
import requests


class Worker(threading.Thread):
    def __init__(self, logger: logging.Logger, opentsdb_param: dict, name: str = "Worker"):
        super(Worker, self).__init__()
        self.__name = name
        self.__queue = []
        self.__logger = logger
        self.__logger.info("Worker {0} created".format(name))
        self.__opentsdb_param = opentsdb_param

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
            data_station = item.station.metrics_history[-1].to_dict()
            data_station["station_uuid"] = str(item.station.uuid)
            for hive in item.station.hive_collection:
                hive.generate_data(item.timestamp)
                self.__logger.info("Worker {0} processed {1} from station {2}".format(self.name,
                                                                                      hive.uuid,
                                                                                      item.station.uuid))
            self.__logger.info("Worker {0} finished {1}".format(self.name, item.station.uuid))
            data_hives = item.station.hive_collection.collect_data()
            self.__logger.info("Worker {0} has {1} items remaining in queue".format(self.name, len(self.__queue)))
            request = self.__generate_request(data_station, data_hives)
            self.__send_request(request)
        self.__logger.info("Worker {0} finished".format(self.name))

    def add(self, item: QueuedItem):
        self.__logger.debug("Worker {0} added station {1} for timestamp {2}".format(self.name,
                                                                                    item.station.uuid,
                                                                                    item.timestamp))
        self.__queue.append(item)

    def __generate_request(self, data_station: dict, data_hive: dict):
        self.__logger.debug("Worker {0} generating request".format(self.name))
        request = []
        for hive in data_hive:
            temperature = {
                "metric": "hive.temperature",
                "timestamp": hive["timestamp"],
                "value": hive["temperature"],
                "tags": {
                    "hive_uuid": hive["hive_uuid"],
                }
            }
            request.append(temperature)
            sound_level = {
                "metric": "hive.sound_level",
                "timestamp": hive["timestamp"],
                "value": hive["sound_level"],
                "tags": {
                    "hive_uuid": hive["hive_uuid"],
                }
            }
            request.append(sound_level)
            weight = {
                "metric": "hive.weight",
                "timestamp": hive["timestamp"],
                "value": hive["weight"],
                "tags": {
                    "hive_uuid": hive["hive_uuid"],
                }
            }
            request.append(weight)

        temperature = {
            "metric": "station.temperature",
            "timestamp": data_station["timestamp"],
            "value": data_station["temperature"],
            "tags": {
                "station_uuid": data_station["station_uuid"],
            }
        }
        request.append(temperature)

        sun = {
            "metric": "station.sun",
            "timestamp": data_station["timestamp"],
            "value": data_station["sun"],
            "tags": {
                "station_uuid": data_station["station_uuid"],
            }
        }
        request.append(sun)

        battery_state = {
            "metric": "station.battery_state",
            "timestamp": data_station["timestamp"],
            "value": data_station["battery_state"],
            "tags": {
                "station_uuid": data_station["station_uuid"],
            }
        }
        request.append(battery_state)

        rain = {
            "metric": "station.rain",
            "timestamp": data_station["timestamp"],
            "value": data_station["rain"],
            "tags": {
                "station_uuid": data_station["station_uuid"],
            }
        }
        request.append(rain)

        wind = {
            "metric": "station.wind",
            "timestamp": data_station["timestamp"],
            "value": data_station["wind"],
            "tags": {
                "station_uuid": data_station["station_uuid"],
            }
        }
        request.append(wind)

        return request

    def __send_request(self, request):
        self.__logger.debug("Worker {0} sending request".format(self.name))
        requests.post("http://" + self.__opentsdb_param["host"]
                     + ":" + str(self.__opentsdb_param["port"]) + "/api/put", json=request)


import threading
import logging
import time
from prometheus_client import start_http_server, Gauge, Counter


class MetricsExporter(threading.Thread):
    def __init__(self, list_stations: list, logger: logging.Logger, port: int = 8000):
        super(MetricsExporter, self).__init__()
        self.__port = port
        self.__list_hives = []
        self.__list_stations = list_stations
        for station in self.__list_stations:
            self.__list_hives.extend(station.hive_collection)
        self.__logger = logger
        self.__logger.info("Exporter created")
        # Start up the server to expose the metrics.
        start_http_server(port)
        # Create a metric to track time spent and requests made.
        self.__METRICS_POINT = Counter('metrics_point', 'Number of metrics points')
        self.__METRICS_POINT_LATENCY = Gauge('metrics_point_latency_seconds', 'Time spent processing request')
        self.__HIVE_TEMPERATURE = Gauge('hive_temperature', 'Temperature of hive', ["hive_uuid"])
        self.__HIVE_SOUND_LEVEL = Gauge('hive_sound_level', 'Sound level of hive', ["hive_uuid"])
        self.__HIVE_WEIGHT = Gauge('hive_weight', 'Weight of hive', ["hive_uuid"])
        self.__STATION_TEMPERATURE = Gauge('station_temperature', 'Temperature of station', ["station_uuid"])
        self.__STATION_BATTERY = Gauge('station_battery', 'Battery of station', ["station_uuid"])
        self.__STATION_RAIN = Gauge('station_rain', 'Rain of station', ["station_uuid"])
        self.__STATION_WIND = Gauge('station_wind', 'Wind of station', ["station_uuid"])
        self.__STATION_SUN = Gauge('station_sun', 'Sun of station', ["station_uuid"])

    def run(self):
        self.__logger.info("Exporter started")
        self.__logger.info("Exporter host: {0}, port: {1}".format("0.0.0.0", self.__port))
        while True:
            start_time = time.time()
            self.__logger.debug("Export data for timestamp {0}".format(time.time()))
            for station in self.__list_stations:
                self.__logger.debug("Export data for station {0}".format(station.uuid))
                self.__STATION_TEMPERATURE.labels(station_uuid=str(station.uuid)).set(station.last_temperature)
                self.__STATION_BATTERY.labels(station_uuid=str(station.uuid)).set(station.last_battery_state)
                self.__STATION_RAIN.labels(station_uuid=str(station.uuid)).set(station.last_rain)
                self.__STATION_WIND.labels(station_uuid=str(station.uuid)).set(station.last_wind)
                self.__STATION_SUN.labels(station_uuid=str(station.uuid)).set(station.last_sun)
                self.__METRICS_POINT.inc()
            for hive in self.__list_hives:
                self.__logger.debug("Export data for hive {0}".format(hive.uuid))
                self.__HIVE_TEMPERATURE.labels(hive_uuid=str(hive.uuid)).set(hive.last_temperature)
                self.__HIVE_SOUND_LEVEL.labels(hive_uuid=str(hive.uuid)).set(hive.last_sound_level)
                self.__HIVE_WEIGHT.labels(hive_uuid=str(hive.uuid)).set(hive.last_weight)
                self.__METRICS_POINT.inc()
            self.__METRICS_POINT_LATENCY.set(time.time() - start_time)
            self.__logger.info("Export data for timestamp {0} done".format(time.time()))

            time.sleep(5 - (time.time() - start_time))


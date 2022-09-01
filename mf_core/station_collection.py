from __future__ import annotations

from uuid import UUID
from time import time
from mf_core.station import Station


class StationCollection(list):
    def __init__(self):
        super().__init__()
        self.__last_collect_timestamp = 0

    def create_station(self) -> UUID:
        """
        Creates a new station and returns its uuid.
        :return:
        """
        station = Station()
        uuid = station.uuid
        self.append(station)
        return uuid

    def collect_data(self) -> list:
        """
        Collects the data from the stations.
        :return:
        """
        data = []
        timestamp = int(time())
        for station in self:
            uuid = str(station.uuid)
            station_data = station.metrics_history.get_lines_between(self.__last_collect_timestamp, timestamp)
            for sd in station_data:
                line = {"station_id": uuid, "timestamp": sd.timestamp, "temperature": sd.temperature, "sun": sd.sun,
                        "rain": sd.rain, "battery_state": sd.battery_state, "wind": sd.wind}
                data.append(line)

        self.__last_collect_timestamp = timestamp if timestamp > self.__last_collect_timestamp else (timestamp + 1)
        return data

    def collect_hives_data(self) -> list:
        """
        Collects the data from the hives.
        :return:
        """
        data = []
        for station in self:
            data.extend(station.hive_collection.collect_data())
        return data

    def get_by_uuid(self, uuid: UUID) -> Station | None:
        """
        Returns the station with the given uuid.
        :param uuid:
        :return:
        """
        for station in self:
            if station.uuid == uuid:
                return station
        return None

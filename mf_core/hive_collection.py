from __future__ import annotations

from uuid import UUID
from mf_core.hive import Hive
from time import time


class HiveCollection(list):
    def __init__(self):
        super().__init__()
        self.__last_collect_timestamp = 0

    def create_hive(self) -> UUID:
        """
        Creates a new hive and returns its uuid.
        :return:
        """
        hive = Hive()
        uuid = hive.uuid
        self.append(hive)
        return uuid

    def collect_data(self) -> list:
        """
        Collects the data from the hives.
        :return:
        """
        data = []
        timestamp = int(time())
        for hive in self:
            uuid = str(hive.uuid)
            hive_data = hive.metrics_history.get_lines_between(self.__last_collect_timestamp, timestamp)
            for hd in hive_data:
                line = {"hive_id": uuid, "timestamp": hd.timestamp, "temperature": hd.temperature, "weight": hd.weight, "sound_level": hd.sound_level}
                data.append(line)

        self.__last_collect_timestamp = timestamp if timestamp > self.__last_collect_timestamp else (timestamp + 1)
        return data

    def get_by_uuid(self, uuid: UUID) -> Hive | None:
        """
        Returns the hive with the given uuid.
        :param uuid:
        :return:
        """
        for hive in self:
            if hive.uuid == uuid:
                return hive
        return None

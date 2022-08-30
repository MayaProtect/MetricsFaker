import random
from uuid import uuid4, UUID
from mf_core.monitored_object import MonitoredObject
from mf_core.metrics_history import MetricsHistory
from mf_core.hive_metrics_history_line import HiveMetricsHistoryLine


class Hive(MonitoredObject):
    """
    Class to create Hive object
    """

    def __init__(self, uuid: UUID = None):
        super().__init__(uuid)
        self.__last_sound_level = 0.0
        self.__last_weight = 0.0

    @property
    def last_sound_level(self) -> float:
        return self.__last_sound_level

    @last_sound_level.setter
    def last_sound_level(self, value: float = 0.0) -> None:
        self.__last_sound_level = value

    @property
    def last_weight(self) -> float:
        return self.__last_weight

    @last_weight.setter
    def last_weight(self, value: float = 0.0) -> None:
        self.__last_weight = value

    def generate_data(self, timestamp: int = 0):
        min_temp = 1000
        max_temp = 4500
        min_weight = 1000000
        max_weight = 10000000
        min_sound_level = 3500
        max_sound_level = 7500

        if len(self.metrics_history) == 0:
            new_temp = (random.randint(min_temp, max_temp) / 100)
            new_weight = (random.randint(min_weight, max_weight) / 100)
            new_sound_level = (random.randint(min_sound_level, max_sound_level) / 100)
        else:
            new_temp = Hive.calc_new_value(self._last_temperature, min_temp, max_temp)
            new_weight = Hive.calc_new_value(self.__last_weight, min_weight, max_weight, 1000)
            new_sound_level = Hive.calc_new_value(self.__last_sound_level, min_sound_level, max_sound_level)

        self.insert_data(new_temp, new_weight, new_sound_level, timestamp)

    def insert_data(self, temperature: float, weight: float, sound_level: float, timestamp: int = 0) -> None:
        """
        Insert new data into hive object

        :param temperature: Temperature
        :param sound_level: Sound level
        :param weight: Weight
        :param timestamp: Timestamp to set
        :return: Nothing
        """
        metrics = HiveMetricsHistoryLine(self._last_temperature, self.__last_weight, self.__last_sound_level, timestamp)
        super().metrics_history.add_data(metrics)
        self._last_temperature = temperature
        self.__last_sound_level = sound_level
        self.__last_weight = weight

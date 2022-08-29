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
        pass

    def insert_data(self, temperature: float, weight: float, sound_level: float) -> None:
        """
        Insert new data into hive object

        :param temperature: Temperature
        :param sound_level: Sound level
        :param weight: Weight
        :return: Nothing
        """
        metrics = HiveMetricsHistoryLine(self._last_temperature, self.__last_weight, self.__last_sound_level)
        super().metrics_history.add_data(metrics)
        self._last_temperature = temperature
        self.__last_sound_level = sound_level
        self.__last_weight = weight

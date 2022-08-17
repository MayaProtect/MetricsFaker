from uuid import uuid4, UUID
from mf_core.metrics_history import MetricsHistory


class Hive:
    """
    Class to create Hive object
    """

    def __init__(self, uuid: UUID = None):
        self.__uuid = uuid if uuid is not None else uuid4()
        self.__last_temperature = 0.0
        self.__last_sound_level = 0.0
        self.__last_weight = 0.0
        self.__metrics_history = MetricsHistory()

    @property
    def uuid(self) -> UUID:
        return self.__uuid

    @property
    def last_temperature(self) -> float:
        return self.__last_temperature

    @last_temperature.setter
    def last_temperature(self, value: float = 0.0) -> None:
        self.__last_temperature = value

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

    @property
    def metrics_history(self) -> MetricsHistory:
        return self.__metrics_history

    def insert_data(self, temperature: float, weight: float, sound_level: float) -> None:
        """
        Insert new data into hive object

        :param temperature: Temperature
        :param sound_level: Sound level
        :param weight: Weight
        :return: Nothing
        """
        self.__metrics_history.add_data(self.__last_temperature, self.__last_weight, self.__last_sound_level)
        self.__last_temperature = temperature
        self.__last_sound_level = sound_level
        self.__last_weight = weight

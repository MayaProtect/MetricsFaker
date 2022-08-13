from uuid import uuid4, UUID


class Hive:
    """
    Class to create Hive object
    """

    def __init__(self, uuid: UUID = None):
        self.__uuid = uuid if uuid is not None else uuid4()
        self.__last_temperature = 0.0
        self.__last_sound_level = 0.0
        self.__last_weight = 0.0

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

from time import time


class MetricsHistoryLine:
    def __init__(self, temperature, weight, sound_level):
        self.__temperature = temperature
        self.__weight = weight
        self.__sound_level = sound_level
        self.__timestamp = int(time())

    @property
    def temperature(self) -> float:
        return self.__temperature

    @property
    def weight(self) -> float:
        return self.__weight

    @property
    def sound_level(self) -> float:
        return self.__sound_level

    @property
    def timestamp(self) -> int:
        return self.__timestamp

    def __str__(self):
        return f"At {self.__timestamp}: Temp={self.__temperature}°C, " \
               f"Weight={self.__weight}g, SoundLevel={self.__sound_level}db"

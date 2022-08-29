from time import time


class MetricsHistoryLine:
    def __init__(self, temperature, timestamp: int = 0):
        self.__temperature = temperature
        self.__timestamp = int(time()) if timestamp == 0 else timestamp

    @property
    def temperature(self) -> float:
        return self.__temperature

    @property
    def timestamp(self) -> int:
        return self.__timestamp

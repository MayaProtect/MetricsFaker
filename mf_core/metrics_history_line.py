from time import time


class MetricsHistoryLine:
    def __init__(self, temperature):
        self.__temperature = temperature
        self.__timestamp = int(time())

    @property
    def temperature(self) -> float:
        return self.__temperature

    @property
    def timestamp(self) -> int:
        return self.__timestamp

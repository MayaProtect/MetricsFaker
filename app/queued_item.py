from mf_core import Station


class QueuedItem:
    def __init__(self, station, timestamp: int = 0):
        self.__station = station
        self.__timestamp = timestamp

    @property
    def station(self):
        return self.__station

    @property
    def timestamp(self):
        return self.__timestamp

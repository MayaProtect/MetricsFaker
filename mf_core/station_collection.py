from uuid import UUID
from mf_core.station import Station

class StationCollection(list):
    def __init__(self):
        super().__init__()
        self.__last_collect_timestamp = 0

    def create_station(self) -> UUID:
        station = Station()
        uuid = station.uuid
        self.append(station)
        return uuid

    def collect_data(self) -> list:
        pass

    def collect_hives_data(self) -> list:
        pass

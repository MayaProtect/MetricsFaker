from mf_core.monitored_object import MonitoredObject
from mf_core.station_metrics_history_line import StationMetricsHistoryLine
from mf_core.hive_collection import HiveCollection
from uuid import UUID


class Station(MonitoredObject):

    def __init__(self, uuid: UUID = None):
        super().__init__(uuid)
        self.__last_sun = 0.0
        self.__last_wind = 0.0
        self.__last_battery_state = 0.0
        self.__last_rain = 0.0
        self.__hive_collection = HiveCollection()

    @property
    def last_sun(self) -> float:
        return self.__last_sun

    @last_sun.setter
    def last_sun(self, value: float) -> None:
        self.__last_sun = value

    @property
    def last_wind(self) -> float:
        return self.__last_wind

    @last_wind.setter
    def last_wind(self, value: float) -> None:
        self.__last_wind = value

    @property
    def last_rain(self) -> float:
        return self.__last_rain

    @last_rain.setter
    def last_rain(self, value: float) -> None:
        self.__last_rain = value

    @property
    def last_battery_state(self):
        return self.__last_battery_state

    @last_battery_state.setter
    def last_battery_state(self, value: float) -> None:
        self.__last_battery_state = value

    @property
    def hive_collection(self):
        return self.__hive_collection

    def insert_data(self, temp: float, sun: float, battery: float, wind: float, rain: float):
        metrics = StationMetricsHistoryLine(self._last_temperature, self.__last_sun, self.__last_battery_state, self.__last_wind, self.__last_rain)
        super().metrics_history.add_data(metrics)
        self._last_temperature = temp
        self.__last_sun = sun
        self.__last_battery_state = battery
        self.__last_wind = wind
        self.__last_rain = rain

from random import randint

from mf_core.monitored_object import MonitoredObject
from mf_core.station_metrics_history_line import StationMetricsHistoryLine
from mf_core.hive_collection import HiveCollection
from mf_core.owner import Owner
from uuid import UUID


class Station(MonitoredObject):

    def __init__(self, uuid: UUID = None):
        super().__init__(uuid)
        self.__last_sun = 0.0
        self.__last_wind = 0.0
        self.__last_battery_state = 0.0
        self.__last_rain = 0.0
        self.__hive_collection = HiveCollection()
        self.__owner = None

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

    @property
    def owner(self) -> Owner:
        return self.__owner

    @owner.setter
    def owner(self, value: Owner):
        self.__owner = value

    def insert_data(self, temp: float, sun: float, battery: float, wind: float, rain: float, timestamp: int = 0):
        """
        Inserts the data into the station metrics history.
        :param temp:
        :param sun:
        :param battery:
        :param wind:
        :param rain:
        :param timestamp:
        :return:
        """
        metrics = StationMetricsHistoryLine(self._last_temperature, self.__last_sun, self.__last_battery_state,
                                            self.__last_wind, self.__last_rain, timestamp)
        super().metrics_history.add_data(metrics)
        self._last_temperature = temp
        self.__last_sun = sun
        self.__last_battery_state = battery
        self.__last_wind = wind
        self.__last_rain = rain

    def generate_data(self, timestamp: int = 0):
        """
        Generates the data for the station.
        :param timestamp:
        :return:
        """
        min_temp = 1000
        max_temp = 4500
        min_sun = 1
        max_sun = 100
        min_battery_state = 1
        max_battery_state = 100
        min_wind = 1
        max_wind = 50
        min_rain = 1
        max_rain = 1000

        if len(self.metrics_history) == 0:
            new_temp = randint(min_temp, max_temp) / 100
            new_sun = randint(min_sun, max_sun) / 100
            new_battery_state = randint(min_battery_state, max_battery_state) / 100
            new_wind = randint(min_wind, max_wind) / 100
            new_rain = randint(min_rain, max_rain) / 100
        else:
            new_temp = Station.calc_new_value(self._last_temperature, min_temp, max_temp)
            new_sun = Station.calc_new_value(self.__last_sun, min_sun, max_sun, 1)
            new_battery_state = Station.calc_new_value(self.__last_battery_state, min_battery_state, max_battery_state,
                                                       1)
            new_wind = Station.calc_new_value(self.__last_wind, min_wind, max_wind, 1)
            rand_rain = randint(0, 100) / 100
            new_rain = (self.__last_rain + rand_rain) if (self.__last_rain + rand_rain) <= max_rain else max_rain

        self.insert_data(new_temp, new_sun, new_battery_state, new_wind, new_rain, timestamp)

    def generate_fake_hive(self) -> None:
        """
        Generates a fake hive for the station.
        """
        uuid_hive = self.__hive_collection.create_hive()
        hive = self.__hive_collection.get_by_uuid(uuid_hive)
        hive.owner = self.owner

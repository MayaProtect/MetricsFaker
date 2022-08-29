from mf_core.metrics_history_line import MetricsHistoryLine


class StationMetricsHistoryLine(MetricsHistoryLine):
    def __init__(self, temperature, sun, battery, wind, rain):
        super().__init__(temperature)
        self.__sun = sun
        self.__battery_state = battery
        self.__wind = wind
        self.__rain = rain

    @property
    def sun(self):
        return self.__sun

    @property
    def battery_state(self):
        return self.__battery_state

    @property
    def wind(self):
        return self.__wind

    @property
    def rain(self):
        return self.__rain

    def __str__(self):
        return f"At {super().timestamp}: Temp={super().temperature}°C, " \
               f"Sun={self.__sun}%, Battery={self.__battery_state}%, " \
               f"Wind={self.__wind}m/s, Rain={self.__rain}mm"

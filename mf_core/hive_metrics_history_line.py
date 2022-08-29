from mf_core.metrics_history_line import MetricsHistoryLine


class HiveMetricsHistoryLine(MetricsHistoryLine):
    def __init__(self, temperature, weight, sound_level, timestamp: int = 0):
        super().__init__(temperature, timestamp)
        self.__weight = weight
        self.__sound_level = sound_level

    @property
    def weight(self) -> float:
        return self.__weight

    @property
    def sound_level(self) -> float:
        return self.__sound_level

    def __str__(self):
        return f"At {super().timestamp}: Temp={super().temperature}°C, " \
               f"Weight={self.__weight}g, SoundLevel={self.__sound_level}db"
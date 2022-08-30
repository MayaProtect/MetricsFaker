from random import randint
from uuid import uuid4, UUID
from mf_core.metrics_history import MetricsHistory


class MonitoredObject:
    def __init__(self, uuid: UUID = None):
        self._uuid = uuid if uuid is not None else uuid4()
        self._last_temperature = 0.0
        self._metrics_history = MetricsHistory()

    @property
    def uuid(self) -> UUID:
        return self._uuid

    @property
    def last_temperature(self) -> float:
        return self._last_temperature

    @last_temperature.setter
    def last_temperature(self, value: float = 0.0) -> None:
        self._last_temperature = value

    @property
    def metrics_history(self) -> MetricsHistory:
        return self._metrics_history

    @metrics_history.setter
    def metrics_history(self, value: MetricsHistory) -> None:
        self._metrics_history = value

    @staticmethod
    def calc_new_value(last_value, min_value, max_value, delta: int = 10):
        new_value = (randint(int(last_value * 100) - delta,
                             int(last_value * 100) + delta) / 100)

        if new_value < (min_value / 100):
            new_value = min_value / 100

        if new_value > (max_value / 100):
            new_value = max_value / 100

        return new_value

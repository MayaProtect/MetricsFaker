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

from mf_core.metrics_history_line import MetricsHistoryLine


class MetricsHistory(list):
    def add_data(self, temperature: float, weight: float, sound_level: float) -> None:
        data_metric = MetricsHistoryLine(temperature, weight, sound_level)
        self.append(data_metric)

    def __getitem__(self, item) -> MetricsHistoryLine:
        return super().__getitem__(item)

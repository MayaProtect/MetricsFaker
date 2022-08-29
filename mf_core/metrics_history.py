from __future__ import annotations
from time import time

from mf_core.metrics_history_line import MetricsHistoryLine


class MetricsHistory(list):
    def add_data(self, metrics: MetricsHistoryLine) -> None:
        """
        Insert a new line in history

        :param metrics: Metrics to add
        :return: Nothing
        """
        self.append(metrics)

    def get_lines_between(self, timestamp_start: int, timestamp_end: int = 0) -> MetricsHistory:
        if timestamp_end == 0:
            timestamp_end = time()

        metrics_lines_to_return = MetricsHistory()
        for i in range(len(self)):
            if timestamp_start <= self[i].timestamp <= timestamp_end:
                metrics_lines_to_return.append(self[i])

        return metrics_lines_to_return

    def __getitem__(self, item) -> MetricsHistoryLine:
        return super().__getitem__(item)

    def append(self, __object: MetricsHistoryLine) -> None:
        return super().append(__object)

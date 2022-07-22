import logging
import requests
import time
from typing import Dict, Iterable

import prometheus_client

from . import hdsentinel, data_types

logger = logging.getLogger(__name__)


class Metrics:
    def __init__(self, gauge_name_unit: Dict[str, str]):
        self.gauges = {
            metric_name: prometheus_client.Gauge(
                name=f'HDS_{metric_name}_{metric_unit}'.lower(),
                documentation=f'HDSentinel {metric_name}',
                labelnames=['disk_id', 'host'],
            )
            for metric_name, metric_unit in gauge_name_unit.items()
        }

    def clear_metrics(self):
        for metric in self.gauges.values():
            metric.clear()

    def update_metrics(self, host_name: str, disk_summaries: Iterable[data_types.HardDiskSummary]):
        self.clear_metrics()

        for disk_summary in disk_summaries:
            for metric_name, metric in self.gauges.items():
                metric.labels(
                    disk_id=disk_summary.disk_id,
                    host=host_name,
                ).set(getattr(disk_summary, metric_name))


def start_server(hdsentinel_client: hdsentinel.HDSentinel, update_interval: int):
    exposed_metrics = Metrics({
        'Current_Temperature': 'celsius',
        'Daily_Average': 'celsius',
        'Daily_Maximum': 'celsius',
        'Health': 'ratio',
        'Performance': 'ratio',
    })

    prometheus_client.start_http_server(8002)

    while True:
        try:
            xml = hdsentinel_client.fetch_xml()
        except (requests.exceptions.ConnectionError, hdsentinel.FetchError) as e:
            logger.error('Failed to fetch HDSentinel XML: %s', e)
            exposed_metrics.clear_metrics()
            continue

        disk_summaries = hdsentinel_client.parse_xml(xml)
        exposed_metrics.update_metrics(hdsentinel_client.host, disk_summaries)
        time.sleep(update_interval)

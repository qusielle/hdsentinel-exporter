import logging
import requests
import time
from typing import Dict, Iterable

import prometheus_client

from . import data_types, hdsentinel, settings

logger = logging.getLogger(__name__)

EXPOSED_METRICS = {
    'Current_Temperature': 'celsius',
    'Daily_Average': 'celsius',
    'Daily_Maximum': 'celsius',
    'Health': 'ratio',
    'Performance': 'ratio',
}


def _compose_metric_name(name: str, unit: str) -> str:
    return f'HDS_{name}_{unit}'.lower()


class Metrics:
    def __init__(self, gauge_name_unit: Dict[str, str]):
        self.gauges = {
            metric_name: prometheus_client.Gauge(
                name=_compose_metric_name(metric_name, metric_unit),
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


def start_server(hdsentinel_client: hdsentinel.HDSentinel):
    exposed_metrics = Metrics(EXPOSED_METRICS)

    logger.info('Starting exporter webservice on %d port', settings.exporter_port)
    prometheus_client.start_http_server(settings.exporter_port)

    while True:
        try:
            xml = hdsentinel_client.fetch_xml()
        except (requests.exceptions.ConnectionError, hdsentinel.FetchError) as e:
            logger.error('Failed to fetch HDSentinel XML: %s', e)
            exposed_metrics.clear_metrics()
        else:
            disk_summaries = hdsentinel_client.parse_xml(xml)
            exposed_metrics.update_metrics(hdsentinel_client.host, disk_summaries)
        finally:
            time.sleep(settings.interval)

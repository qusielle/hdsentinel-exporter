import logging
import requests
import time

import prometheus_client

from . import hdsentinel

logger = logging.getLogger(__name__)


def init_metrics(metric_names: list) -> dict:
    return {
        metric_name: prometheus_client.Gauge(
            name=f'HDS_{metric_name}',
            documentation=f'HDSentinel {metric_name}',
            labelnames=['disk_id'],
        )
        for metric_name in metric_names
    }


def update_metrics(disk_summaries, exposed_metrics):
    clear_metrics(exposed_metrics)

    for disk_summary in disk_summaries:
        for metric_name, metric in exposed_metrics.items():
            metric.labels(
                disk_id=disk_summary.disk_id
            ).set(getattr(disk_summary, metric_name))


def clear_metrics(exposed_metrics):
    for metric in exposed_metrics.values():
        metric.clear()


def start_server(hdsentinel_client: hdsentinel.HDSentinel, update_interval: int):
    exposed_metrics = init_metrics([
        'Current_Temperature',
        'Daily_Average',
        'Daily_Maximum',
        'Health',
        'Performance',
    ])

    prometheus_client.start_http_server(8002)

    while True:
        try:
            xml = hdsentinel_client.fetch_xml()
        except (requests.exceptions.ConnectionError, hdsentinel.FetchError) as e:
            logger.error('Failed to fetch HDSentinel XML: %s', e)
            clear_metrics(exposed_metrics)
            continue

        disk_summaries = hdsentinel_client.parse_xml(xml)
        update_metrics(disk_summaries, exposed_metrics)
        time.sleep(update_interval)

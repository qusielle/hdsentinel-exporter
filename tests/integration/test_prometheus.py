import pathlib
import socket
import unittest.mock

import pytest
import requests
from prometheus_client.parser import text_string_to_metric_families

import hdsentinel_exporter.hdsentinel
import hdsentinel_exporter.prometheus
from hdsentinel_exporter import settings


class ExecutionFlowControlException(Exception):
    """Exception to check the exectuion flow is going as planned in the test."""


def _find_free_port(start_port: int = 8859) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        for port in range(start_port, 65535):
            if s.connect_ex(('localhost', port)):
                print(f'Found free port: {port}')
                return port

    raise ConnectionError('Could not find a free port to test!')


def test_start_server(monkeypatch, hdsentinel_xml_file_path: pathlib.Path):
    host = 'test_host'
    port = 'test_port'

    settings.interval = 0
    settings.exporter_port = _find_free_port()

    hdsentinel_obj = hdsentinel_exporter.hdsentinel.HDSentinel(host, port)

    with open(hdsentinel_xml_file_path, 'rb') as f:
        reference_xml = f.read()

    def fetch_side_effect():
        yield reference_xml
        while True:
            yield ExecutionFlowControlException

    mock_fetch_xml = unittest.mock.MagicMock(side_effect=fetch_side_effect())

    monkeypatch.setattr(hdsentinel_obj, 'fetch_xml', mock_fetch_xml)

    with pytest.raises(ExecutionFlowControlException):
        hdsentinel_exporter.prometheus.start_server(hdsentinel_obj)

    exposed_page_text = requests.get(f'http://localhost:{settings.exporter_port}/metrics').text

    actual_metrics = text_string_to_metric_families(exposed_page_text)
    actual_metric_names = set(i.name for i in actual_metrics)

    expected_metric_names = set(
        hdsentinel_exporter.prometheus._compose_metric_name(name, unit)
        for name, unit in hdsentinel_exporter.prometheus.EXPOSED_METRICS.items()
    )

    assert actual_metric_names >= expected_metric_names

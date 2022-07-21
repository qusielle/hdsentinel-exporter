from typing import Dict, Generator

import lxml.etree
import requests

from . import data_types


class HDSentinelError(Exception):
    """Base exception occuring during HDSentinel operations."""


class FetchError(HDSentinelError):
    """Data fetch error."""


class ParseError(HDSentinelError):
    """XML parse error."""


def xml_children_as_dict(xml_element: lxml.etree._Element) -> Dict[str, str]:
    return {i.tag: i.text for i in xml_element.getchildren()}


class HDSentinel:
    def __init__(self, host: str, port: str):
        self.host = host
        self.port = port

    def fetch_xml(self) -> bytes:
        xml_url = f'http://{self.host}:{self.port}/xml'
        response = requests.get(xml_url)
        if not response.ok:
            raise FetchError(f'HTTP error {response.status_code} while fetching {xml_url}.')
        return response.content

    def parse_xml(self, xml_data: bytes) -> Generator[data_types.HardDiskSummary, None, None]:
        parsed_xml = lxml.etree.fromstring(xml_data)
        if parsed_xml.tag != 'Hard_Disk_Sentinel':
            raise ParseError('HDSentinel XML does not start with `Hard_Disk_Sentinel` tag.')

        for summary_xml in parsed_xml.findall('.//Hard_Disk_Summary'):
            summary_dict = xml_children_as_dict(summary_xml)
            transformed_summary = data_types.HardDiskSummary(**summary_dict)
            yield transformed_summary

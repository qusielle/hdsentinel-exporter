import requests


class HDSentinelError(Exception):
    """Base exception occuring during HDSentinel operations."""


class FetchError(HDSentinelError):
    """Data fetch error."""


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

    def parse_xml(self, xml_data: bytes):
        return xml_data

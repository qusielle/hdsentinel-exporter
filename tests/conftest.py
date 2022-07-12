"""Common Pytest setup for tests."""
import pathlib

import pytest


DATA_DIR = pathlib.Path(__file__).parent / 'data'


@pytest.fixture(params=DATA_DIR.glob('*'))
def hdsentinel_xml_file(request):
    return request.param

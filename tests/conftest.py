"""Common Pytest setup for tests."""
import os
import pathlib

import pytest


DATA_DIR = pathlib.Path(__file__).parent / 'data'


def pytest_configure():
    pytest.update_output_data = bool(os.getenv('UPDATE_DATA'))


@pytest.fixture(params=DATA_DIR.glob('*.xml'))
def hdsentinel_xml_file_path(request):
    return request.param

import json
import pathlib

import pytest

import hdsentinel_exporter.hdsentinel


def test_parse_xml(hdsentinel_xml_file_path: pathlib.Path):
    host = 'test_host'
    port = 'test_port'
    hdsentinel_output_reference_path = (
        hdsentinel_xml_file_path.parent / (hdsentinel_xml_file_path.name + '.out.json')
    )

    hdsentinel_obj = hdsentinel_exporter.hdsentinel.HDSentinel(host, port)

    with open(hdsentinel_xml_file_path, 'rb') as f:
        summary_generator = hdsentinel_obj.parse_xml(f.read())

    dumpable_summary = [i.dict() for i in summary_generator]

    if pytest.update_output_data:
        with open(hdsentinel_output_reference_path, 'w') as f:
            json.dump(dumpable_summary, f, indent=1)

    with open(hdsentinel_output_reference_path) as f:
        expected_summary = json.load(f)

    assert dumpable_summary == expected_summary

import hdsentinel_exporter.hdsentinel


def test_parse_xml(hdsentinel_xml_file):
    host = 'test_host'
    port = 'test_port'

    obj = hdsentinel_exporter.hdsentinel.HDSentinel(host, port)

    assert obj.parse_xml(hdsentinel_xml_file)

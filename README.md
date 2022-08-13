# HDSentinel Exporter

HDSentinel Exporter is a [Prometheus] exporter that provides info about SSD and
HDD generated by [HDSentinel] (other name: Hard Disk Sentinel).

Only the Windows version of HDSentinel is supported for now.

## HDSentinel preparation

In order to get everything working, you need to enable WebStatus page in
HDSentinel. For that, in Configuration window, in Integration tab, select
`Enable WebStatus` and set a port (default is `61220`, same in the exporter).

Check the availability of `WebStatus` by accessing
`http://<YOUR_IP>:<PORT>/xml`.

## Usage

### Running from source

This project uses [Pipenv] for dependency handling, so install it first and
prepare the environment:

```bash
python3 -m pip install pipenv
pipenv sync
```

Then you can run the `hdsentinel_exporter` module:

```bash
pipenv run python -m hdsentinel_exporter --help
```

The usage is as following:

```
usage: hdsentinel_exporter [-h] [--host HOST] [--port PORT] [--debug]
                           [--interval INTERVAL]
                           [--exporter-port EXPORTER_PORT]

Prometheus exporter for HDSentinel harddisk data. Every CLI option is
available to be set in env by the name preppended by `HDS_EXP_`. For example,
`--exporter-port` becomes `HDS_EXP_EXPORTER_PORT` env variable.

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           HDSentinel host address (default: localhost)
  --port PORT           HDSentinel port (default: 61220)
  --debug               show debug output (default: False)
  --interval INTERVAL   data fetching interval in seconds (default: 10)
  --exporter-port EXPORTER_PORT
                        exporter webservice port (default: 9958)
```

For example, if run the exporter on the address `192.168.0.100`, you may expect
a similar output:

```bash
$ pipenv run python -m hdsentinel_exporter --host 192.168.0.100 --debug
Starting exporter webservice on 9958 port
DEBUG: hdsentinel.py:35 fetch_xml: Fetching: http://192.168.0.100:61220/xml
DEBUG: hdsentinel.py:42 parse_xml: Parsing XML (161152 bytes)
```

### Running the Docker image

To build the image:

```bash
docker build -t hdsentinel_exporter .
```

All CLI arguments can be specified by a corresponding environmental variable, so
the example from the previous paragraph is like the following when calling in
Docker:

```bash
docker run -e HDS_EXP_HOST=192.168.0.100 -e HDS_EXP_DEBUG=true -p 9958:9958 hdsentinel_exporter
```

An example Prometheus [Docker Compose] service YAML may look like this:

```yaml
  hdsentinel:
    image: hdsentinel_exporter:latest
    container_name: hdsentinel
    ports:
      - "9959:9958"
    environment:
      - HDS_EXP_HOST=192.168.0.100
      - HDS_EXP_DEBUG=true
    restart: unless-stopped
    networks:
      - monitor-net
    labels:
      org.label-schema.group: monitoring

```

## Provided metrics

Metrics currently exposed are:

| Name                            | Type  | Unit    | Help                           |
| ------------------------------- | ----- | ------- | ------------------------------ |
| hds_current_temperature_celsius | Gauge | Celsius | HDSentinel Current_Temperature |
| hds_daily_average_celsius       | Gauge | Celsius | HDSentinel Daily_Average       |
| hds_daily_maximum_celsius       | Gauge | Celsius | HDSentinel Daily_Maximum       |
| hds_health_ratio                | Gauge | Ratio   | HDSentinel Health              |
| hds_performance_ratio           | Gauge | Ratio   | HDSentinel Performance         |


## Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

The source code is licensed under the GNU GPLv3 license, which you can find in
the [LICENSE](LICENSE) file.


[Docker Compose]: https://docs.docker.com/compose/
[Prometheus]: https://prometheus.io/
[HDSentinel]: https://www.hdsentinel.com/
[Pipenv]: https://pipenv.pypa.io/en/latest/

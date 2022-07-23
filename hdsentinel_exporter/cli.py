import argparse

from . import settings


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog='hdsentinel_exporter',
        description="""
            Prometheus exporter for HDSentinel harddisk data.
            Every CLI option is available to be set in env by the name
            preppended by `HDS_EXP_`.
            For example, `--exporter-port` becomes `HDS_EXP_EXPORTER_PORT`
            env variable.
        """
    )

    parser.add_argument(
        '--host',
        default=settings.host,
        help='HDSentinel host address',
    )
    parser.add_argument(
        '--port',
        default=settings.port,
        help='HDSentinel port',
    )
    parser.add_argument(
        '--debug',
        default=settings.debug,
        action='store_true',
        help='show debug output',
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=settings.interval,
        help='data fetching interval in seconds',
    )
    parser.add_argument(
        '--exporter-port',
        type=int,
        default=settings.exporter_port,
        help='exporter webservice port',
    )

    return parser.parse_args()

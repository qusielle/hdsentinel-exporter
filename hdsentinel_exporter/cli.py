import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        'host',
        help='HDSentinel host address',
    )
    parser.add_argument(
        '--port',
        default='61220',
        help='HDSentinel port',
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='show debug output',
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=10,
        help='data fetching interval in seconds',
    )
    parser.add_argument(
        '--exporter-port',
        type=int,
        default=9958,
        help='exporter webservice port',
    )

    return parser.parse_args()

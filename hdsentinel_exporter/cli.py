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

    return parser.parse_args()

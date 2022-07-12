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

    return parser.parse_args()

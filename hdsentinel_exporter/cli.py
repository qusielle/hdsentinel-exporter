import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "host",
        help="HDSentinel host address",
    )

    return parser.parse_args()

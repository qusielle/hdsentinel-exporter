#!/usr/bin/env python3
import logging
import sys

from . import cli, hdsentinel, prometheus


class LogFormatter(logging.Formatter):
    format_lookup = {
        logging.DEBUG: '%(levelname)s: %(filename)s:%(lineno)d %(funcName)s: %(message)s',
        logging.INFO: '%(message)s',
        logging.WARN: '%(levelname)s: %(message)s',
        logging.ERROR: '%(levelname)s:\n%(message)s\n',
        logging.CRITICAL: '%(levelname)s:\n%(message)s\n',
    }

    def format(self, record):
        orig_format = self._style._fmt
        try:
            self._style._fmt = self.format_lookup.get(record.levelno, orig_format)
            return super().format(record)
        finally:
            self._style._fmt = orig_format


def init_logging(debug: bool):
    logging_handler = logging.StreamHandler(sys.stdout)
    logging_handler.setFormatter(LogFormatter())
    logging.root.addHandler(logging_handler)
    logging.root.setLevel(logging.DEBUG if debug else logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def main():
    args = cli.parse_args()

    init_logging(args.debug)
    logger = logging.getLogger(__name__)

    hdsentinel_client = hdsentinel.HDSentinel(args.host, args.port)

    try:
        prometheus.start_server(hdsentinel_client, args.interval)
    except KeyboardInterrupt:
        logger.info('Exiting after a keyboard interrupt.')


if __name__ == "__main__":
    main()

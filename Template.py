#!/usr/bin/python3

import argparse
import logging
from pathlib import Path
from subprocess import DEVNULL, run
from tempfile import TemporaryDirectory

# Temoprary folder
TMP = TemporaryDirectory()
# define logger
FMT = '%(asctime)s %(levelname)-8s %(message)s'
DATEFMT = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(fmt=FMT, datefmt=DATEFMT)
default_level = logging.INFO
TEMP_LOG = 'Temp.log'
import coloredlogs
coloredlogs.install(level=default_level, fmt=FMT, datefmt=DATEFMT)
log_file = logging.FileHandler(TEMP_LOG)
log_file.setFormatter(formatter)
log_file.setLevel(default_level)
log = logging.getLogger(__name__)


def function():
    pass


def parse_args():
    arg = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=main.__doc__)
    arg.add_argument('-o', '--out', default='out',
                     help='output directory')
    return arg.parse_args()


def main():
    """
    Docstring.
    """
    arg = parse_args()
    arg.out = Path(arg.out)
    log.info('test')
    log.info(arg)
    # start here
    function()
    # end
    log.info('Bye')


if __name__ == '__main__':
    main()

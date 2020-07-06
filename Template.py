#!/usr/bin/python3

import argparse
import logging
from pathlib import Path
from os import devnull
from tempfile import TemporaryDirectory

# Temoprary folder
TMP = TemporaryDirectory()
NULL = open(devnull, 'w')
# define logger
FMT = '%(asctime)s %(levelname)-8s %(message)s'
DATEFMT = '%H:%M:%S'
TEMP_LOG = 'Temp.log'
logging.basicConfig(format=FMT, datefmt=DATEFMT, level=logging.INFO,
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler(TEMP_LOG)])
try:
    import coloredlogs
    coloredlogs.install(level=logging.INFO, fmt=FMT, datefmt=DATEFMT)
except ImportError:
    pass
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
    log.info('bye')


if __name__ == '__main__':
    main()

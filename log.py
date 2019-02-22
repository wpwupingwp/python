#!/usr/bin/python3

import coloredlogs, logging

fmt = '%(asctime)s %(levelname)s %(message)s'
datefmt = '%I:%M:%S'
logging.basicConfig(level=logging.INFO, format=fmt, datefmt=datefmt,
                    handlers=[logging.FileHandler('test.log', 'w'), ])
coloredlogs.install(level='INFO', fmt=fmt, datefmt=datefmt)
log = logging.getLogger(__name__)
log.info('start')
log.critical('Cannot find it.')
try:
    a = 1 / 0
except Exception:
    log.exception('test.')
log.info('bye')

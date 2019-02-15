#!/usr/bin/python3

from pyqrcode import create
from sys import argv

a = create(argv[1])
a.png('a.png')

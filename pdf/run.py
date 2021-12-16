#!/usr/bin/python3

from sys import argv
from pathlib import Path

from add_watermark import add_mark
from send_mail import send


pdf = Path(argv[1]).absolute()
mark = Path(argv[2]).absolute()
email = argv[3]

marked_pdf = add_mark(pdf, mark)
send(email, marked_pdf)
#!/usr/bin/python3

from sys import argv
from pathlib import Path

from add_watermark import add_mark
from send_mail import send


pdf = Path(argv[1]).absolute()
# email address as mark
email = argv[2]
key = argv[3]

marked_pdf = add_mark(pdf, email)
send(email, marked_pdf, key)

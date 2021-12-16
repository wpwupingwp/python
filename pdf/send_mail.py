#!/usr/bin/python3

import smtplib
from email.message import EmailMessage


def send(to='', attachment=None, key=''):
    with open(key, 'r', encoding='utf-8') as key:
        server = key.readline().strip()
        port = key.readline().strip()
        username = key.readline().strip()
        password = key.readline().strip()
        subject = key.readline().strip()
        content = key.readline().strip()

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = to
    msg.set_content(content)
    if attachment is not None:
        with open(attachment, 'rb') as _:
            attachment = _.read()
        msg.add_attachment(attachment, maintype='application', subtype='pdf')

    smtp = smtplib.SMTP(host=server, port=port)
    # smtp.connect()
    smtp.starttls()
    smtp.login(username, password)
    smtp.send(msg)
    smtp.quit()
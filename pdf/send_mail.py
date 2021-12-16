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
            attachment_bin = _.read()
            # attachment: Path
        msg.add_attachment(attachment_bin, maintype='application', subtype='pdf', filename=attachment.name)

    smtp = smtplib.SMTP(host=server, port=port)
    # smtp.connect()
    smtp.starttls()
    smtp.login(username, password)
    smtp.send_message(msg)
    smtp.quit()
    print('Email sent.')
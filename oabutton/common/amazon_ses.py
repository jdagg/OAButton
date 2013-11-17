import smtplib

msg = """From: "Open Access Test Account" <oabutton@crankycoder.com>
To: "Victor Ng" <victor@crankycoder.com>
Subject: You don't suck

This is some text.  Just a test
"""
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class AmazonSES(object):
    """
    Wrapper around Amazon SES to send out emails
    """
    def __init__(self):
        self.smtp = smtplib.SMTP(settings.AMAZON_SMTPHOST)
        self.smtp.starttls()
        self.smtp.login(settings.SESSMTPUSERNAME, settings.SESSMTPPASSWORD)

    def send_mail(self, from_addr, to_addrs, cc_addrs, subject, msg_text, msg_html):
        if isinstance(to_addrs, basestring):
            to_addrs = [to_addrs, ]
        if isinstance(cc_addrs, basestring):
            cc_addrs = [cc_addrs, ]

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = settings.OABUTTON_EMAIL
        msg['CC'] = ', '.join(cc_addrs)
        msg['To'] = ', '.join(to_addrs)

        part1 = MIMEText(msg_text, 'plain')
        part2 = MIMEText(msg_html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        self.smtp.sendmail(from_addr,
                           to_addrs + cc_addrs,
                           msg.as_string())

#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 metawirl <metaswirl@gmail.com>
#
# Distributed under terms of the MIT license.

""" """
import sys
import os
import argparse
import smtplib
from getpass import getpass
DEBUG=False

def error_print(msg):
    sys.stderr.write("ERROR: {:}\n".format(msg))

def debug_print(msg):
    if DEBUG: sys.stderr.write("DEBUG: {:}\n".format(msg))

def main():
    sender = "nsemmler@inet.tu-berlin.de"
    receivers = ["metaswirl@gmail.com"]

    message = """From: Niklas <nsemmler@inet.tu-berlin.de>
To: Niklas <metaswirl@gmail.com>
Subject: SMTP e-mail test

This is a test e-mail message.
    """
    password = getpass()
    try:
        smtpObj = smtplib.SMTP_SSL(timeout=5)
        smtpObj.set_debuglevel(True)
        smtpObj.connect(host="mail.inet.tu-berlin.de")
        smtpObj.login("nsemmler", password)
        smtpObj.sendmail(sender, receivers, message)
        print "Successfully sent email"
    except smtplib.SMTPException:
        print "Error: unable to send email"
    else:
        smtpObj.quit()

if __name__ == '__main__':
    main()

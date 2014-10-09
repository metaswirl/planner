#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 metawirl <metaswirl@gmail.com>
#
# Distributed under terms of the MIT license.
# TODO: set sender name and email by environment variables

""" """
import sys
import os
import shutil
import smtplib
import subprocess
import tempfile
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

DEBUG=True
INFO=True

def err_print(msg):
    sys.stderr.write("ERROR: {:}\n".format(msg))

def dbg_print(msg):
    if DEBUG: sys.stderr.write("DEBUG: {:}\n".format(msg))

def info_print(msg):
    if INFO: sys.stderr.write("INFO: {:}\n".format(msg))

class Mailer(object):
    def __init__(self, host, timeout):
        self._host = host
        self._timeout = timeout

    def mailto(self, author, msg, receivers):
        try:
            smtpObj = smtplib.SMTP_SSL(timeout=self._timeout)
            smtpObj.set_debuglevel(True)
            smtpObj.connect(host=self._host)
            smtpObj.login(author.login, author.password)
            smtpObj.sendmail(author.mail, receivers, msg.as_string())
            print "Successfully sent email"
        except smtplib.SMTPException:
            print "Error: unable to send email"
            # FIXME: Log exception
        else:
            smtpObj.quit()

class Message(object):
    def __init__(self, author, person, templ):
        self.receiver = [person.mail]
        self.msg = MIMEMultipart()
        self.msg["To"] = "{} <{}>".format(person.name, person.mail)
        self.msg["From"] = "{} <{}>".format(author.name, author.mail)
        self.msg["Subject"] = templ.msg_content.format(person)
        self.msg.attach(MIMEText(templ.msg_content.format(person)))

        part = MIMEBase("application", "octet-stream")
        part.set_payload(self._render_pdf(templ))
        encoders.encode_base64(part)
        self.msg.add_header('Content-Disposition', 'attachment',
            filename=templ.mime_filename.format(person=person)
        )
        print(templ.mime_filename.format(person=person))
        self.msg.attach(part)

    def _render_pdf(self, templ):
        temp_dir = tempfile.mkdtemp()
        dbg_print("Created temp dir at {}".format(temp_dir))
        temp_file = os.path.join(temp_dir, templ.mime_filename)
        temp_tex, temp_pdf = temp_file + ".tex", temp_file + ".pdf"

        try:
            dbg_print("Compiling template {}".format(temp_tex))
            with open(temp_tex, "w") as f:
                f.write(templ.mime_data)
            current = os.curdir
            try:
                os.chdir(temp_dir)
                args=["pdflatex", temp_tex, "-halt-on-error"]
                dbg_print("Running: {}".format(" ".join(args)))
                subprocess.check_call(args)
            finally:
                os.chdir(current)
            with open(temp_pdf, "rb") as f:
                mime_data = f.read()
            #with open("/tmp/foo.pdf", "wb") as f:
            #    f.write(mime_data)
            return mime_data
        finally:
            dbg_print("Removing temp dir {}".format(temp_dir))
            shutil.rmtree(temp_dir)

    def compile(self):
        return self.receiver, self.msg

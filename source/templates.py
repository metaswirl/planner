#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 metawirl <metaswirl@gmail.com>
#
# Distributed under terms of the MIT license.

""" """
import os
import re
from mako.template import Template

class Templ(object):
    __slots__ = ["msg_subject", "msg_content", "mime_filename", "_mime_path", "mime_data"]

    def __init__(self, sub, cont, name, path):
        self.msg_subject = sub
        self.msg_content = cont
        self.mime_filename = name
        self.set_mime_path(path)

    def set_mime_path(self, path):
        rpath = os.path.realpath(path)
        if not os.path.exists(rpath):
            raise Exception("Template file {} does not exist.".format(path))
        self._mime_path = rpath

    def compile(self, author, person, schedule):
        self.msg_subject = self.msg_subject.format(author=author, person=person)
        self.msg_content = self.msg_content.format(author=author, person=person)

        templ = Template(filename=self._mime_path,
                        input_encoding='utf-8',
                        output_encoding='utf-8',
                        preprocessor=lambda x: re.sub(r'\\\\', "${'\\\\\\\\\\\\\\'}", x)
        )
        self.mime_data = templ.render(person=person, schedule=schedule)


class TemplTutorPlan(Templ):
    def __init__(self):
        msg_subject = "Einsatzplan Tutoren"
        msg_text = """Hallo {person.name},
anbei_folgt der Einsatzplan für die erste Woche.

Gruß,
{author.name}"""
        mime_path = "../template/tutor_hours.tex.mako"
        mime_fn = "{person.name}_einsatzplan.pdf"
        super(TemplTutorPlan, self).__init__(
            msg_subject, msg_text, mime_fn, mime_path
        )

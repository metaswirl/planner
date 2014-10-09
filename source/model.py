#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 metawirl <metaswirl@gmail.com>
#
# Distributed under terms of the MIT license.

""" """

from getpass import getpass
import datetime

class Person(object):
    __slots__ = ["name", "mail", "job", "hours"]

    def __init__(self, nam, mail, job, hours):
        self.name = nam
        self.mail = mail
        self.job = job
        self.hours = hours

class Schedule(object):
    schedules = []

    def add_entry(self, entry):
        if isinstance(entry, ScheduleEntry):
            self.schedules.append(entry)
        else:
            raise Exception("Only add ScheduleEntries to Schedule")

    def sort_by_date(self):
        return self.schedules


class ScheduleEntry(object):
    __slots__ = ["day", "start", "end", "room", "contact", "task"]

    def __init__(self, day, start, end, room, task, contact):
        self.day = self.set_obj(day, datetime.date)
        self.start = self.set_obj(start, datetime.time)
        self.end = self.set_obj(end, datetime.time)
        self.room = room
        self.task = task
        self.contact = contact

    def set_obj(self, elem, typ):
        if isinstance(elem, typ):
            return elem
        else:
            raise Exception("Only add day as datetime.day objects")

    def duration(self):
        # TODO: calculate duration
        raise NotImplementedError

    @property
    def weekday(self):
        days = {0:"Montag", 1:"Dienstag", 2:"Mittwoch", 3:"Donnerstag",
            4:"Freitag", 5:"Samstag", 6:"Sonntag"}
        return days[self.day.weekday()]

class Author(object):
    __slots__ = ["login", "name", "mail", "password"]

    def __init__(self, login, name, mail):
        self.login = login
        self.name = name
        self.mail = mail
        print("Please enter password for email account: ")
        self.password = getpass()

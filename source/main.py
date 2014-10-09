#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 metawirl <metaswirl@gmail.com>
#
# Distributed under terms of the MIT license.

""" """
import templates
import model
import logic
from datetime import date, time

def main():
    author = model.Author("nsemmler", "Niklas Semmler", "nsemmler@inet.tu-berlin.de")
    person = model.Person("Erika Mustermann", "metaswirl@gmail.com", "Tutor", "60")
    schedule_entry = model.ScheduleEntry(
        date(2014, 10, 9), time(10, 15), time(11, 45),
        "MAR 4.029", "Tutorium", "Niklas"
    )
    schedule = model.Schedule()
    schedule.add_entry(schedule_entry)
    templ = templates.TemplTutorPlan()
    templ.compile(author, person, schedule)
    receivers, msg = logic.Message(author, person, templ).compile()
    mailer = logic.Mailer("mail.inet.tu-berlin.de", 5)
    mailer.mailto(author, msg, receivers)

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
time_slots = [10, 12, 14, 16]

STARTING_DAY = 1  # Class starts on a Tuesday

class Room(object):
    def __init__(self, name):
        self.name = name
        self.booked = [[False]*len(time_slots) for day in weekdays[STARTING_DAY:] + weekdays]
    
    def is_booked(self, week, day, time):
        """
        >>> room = Room("Test Room")
        >>> room.is_booked(1, "Montag", 12)
        False
        >>> room.book(1, "Montag", 12)
        >>> room.is_booked(1, "Montag", 12)
        True
        """
        if time > 8:
            time = time_slots.index(time)
        day_index = calculate_day_index(week, day)
        return self.booked[day_index][time]
    
    def book(self, week, day, time, booked = True):
        """
        Book or unbook the room for the provided time slot.
        """
        time = time_slots.index(time)
        day_index = calculate_day_index(week, day)
        self.booked[day_index][time] = booked
    
    def get_booked_times(self, week, day):
        """
        Returns the time slots the room is booked for in the given week and day.
        """
        day_index = calculate_day_index(week, day)
        return [time for time_index, time in enumerate(time_slots) if self.booked[day_index][time_index]]
    
    def print_booked_time_slots(self):
        """
        Print all booked times for this room.
        """
        for day_index in range(len(self.booked)):
            week, day = get_week_and_day(day_index)
            for slot_index, time in enumerate(time_slots):
                if self.booked[day_index][slot_index]:
                    print "Raum {} ist in der {}. Woche gebucht am {} um {} Uhr.".format(self.name, week, day, time_slots[slot_index])
        

def read_rooms_from_file(file_name):
    """
    This only works for raeume_zentral.csv.
    """
    # read raeume Zentral to a list
    file_as_list = read_file_to_list(file_name)
    
    # generate room objects 
    first_row_index = get_weekday_finder(file_as_list).next()[0] # get row with room names
    room_names = file_as_list[first_row_index][1:]
    rooms = [Room(room_name) for room_name in room_names]
    
    day_finder = get_weekday_finder(file_as_list)
    timetable_offset = 2  # one blank line after weekday line
    
    day_index = 0
    for line_index, day in day_finder:  # Iterate over all the weekday names found by the weekday finder
        for time_index, time in enumerate(time_slots):  # For each weekday found, iterate over the time slots
            booked_list = map(int, file_as_list[line_index + timetable_offset + time_index][1:])
            for room_index, status in enumerate(booked_list):
                if bool(status):
                    day, week = get_week_and_day(day_index)
                    rooms[room_index].book(day, week, time)
        day_index += 1
    return rooms

def get_available_rooms(room_list, week, day, time):
    """
    Returns a list of all rooms in the room_list that are booked for the given time
    slot.
    """
    available_rooms = [room for room in rooms if room.is_booked(week, day, time)]
    return available_rooms

def get_room_by_name(room_list, name):
    """
    Find a room in the room_list by searching for its name.
    """
    for room in room_list:
        if room.name == name:
            return room
    return None

def get_weekday_finder(file_list, day = "Dienstag"):
    """
    Returns a generator that iterates over file_list in search of the next
    weekday string. Returns the index of the next line in the list with the
    next weekday as first element, along with the corresponding weekday.
    Default start day is Tuesday.
    """
    for i, line in enumerate(file_list):
        for day in weekdays:
            if day in line:
                result = i, day
                yield result
                break

def read_file_to_list(filename):
    """
    Reads a file to a list line by line. Removes whitespace from entries.
    Converts suitable entries to integers
    """
    with open(filename) as f:
        # read csv file:
        file_as_list = [line.strip().split("\t") for line in f.readlines()]
        # remove whitespace:
        file_as_list = [[entry.strip() for entry in line] for line in file_as_list]
        return file_as_list
        
def calculate_day_index(week, day, first_week_offset = STARTING_DAY):
    """
    Given the week (either 1 or 2) and the name of the weekday, this method calculates the corresponding index in the 
    booked array.
    >>> calculate_day_index(1, "Dienstag", first_week_offset = 1)
    0
    >>> calculate_day_index(2, "Montag", first_week_offset = 0)
    5
    """
    day_index = weekdays.index(day)
    if week == 2:
        day_index += len(weekdays) - first_week_offset
    else:
        day_index -= first_week_offset
    return day_index

def get_week_and_day(day_index, first_week_offset = STARTING_DAY):
    """
    Given the number of days since Tuesday in week one, this method calculates the corresponding week and weekday in the 
    booked array and returns them as a (int, string) tuple.
    >>> get_week_and_day(0, first_week_offset=1)
    (1, 'Dienstag')
    >>> get_week_and_day(4, first_week_offset=1)
    (2, 'Montag')
    """
    if day_index >= len(weekdays) - first_week_offset:
        week = 2
    else:
        week = 1
    return week, weekdays[(day_index + first_week_offset) % len(weekdays)]


if __name__=="__main__":   
    import doctest
    doctest.testmod()
     
    # Read the file to list of rooms:
    rooms = read_rooms_from_file("../csv/raeume/raeume_zentral.csv")

    test_room = get_room_by_name(rooms, "MAR 0.001")
    test_room.print_booked_time_slots()
    
    
    for time in time_slots:
        print test_room.is_booked(1, "Montag", time)
        
    print test_room.get_booked_times(1, "Donnerstag")
    print [room.name for room in get_available_rooms(rooms, 1, "Dienstag", 12)]

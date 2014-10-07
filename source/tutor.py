#!/usr/bin/env python
# -*- coding: utf-8 -*-

keys = ["Name", "Vorname", "E-Mail", "Fachgebiet", "Mobil", 
        "Monatsstunden", "C-Kenntnisse", "Unsicherheit", "Verfuegbar"]


class Tutor(object):
    def __init__(self, filename):
        """
        Create a new tutor and parse the .csv file to the data dictionary.
        """
        self.data = dict(zip(keys, [None]*len(keys))) # setup empty dictionary
        
        # parse file to list:
        with open(filename) as f:
            self.file_as_list = [line.strip().split("\t") for line in f.readlines()]  # clear whitespace, split tabs
            self.file_as_list = [line for line in self.file_as_list if not line == [""]]  # discard empty lines
            self.file_as_list = [[entry.strip('"') for entry in line] for line in self.file_as_list]  # strip quotation marks
                  
        # find out where timetable begins:
        timetable_offset = self.file_as_list.index(["Mo.", "Di.", "Mi.", "Do.", "Fr."]) + 1
        
        # fill in basic fields:
        for line in self.file_as_list[:timetable_offset - 2]:  # these lines should contain one entry per line
            key = line[0].split(" ")[0]  # Simplify names of keys to first word
            if key in keys and len(line) > 1:
                if key in ["Monatsstunden", "C-Kenntnisse", "Unsicherheit"]:
                    self.data[key] = int(line[1])  # Convert to integers where appropriate
                else:
                    self.data[key] = line[1]
        
        # fill in availability:
        def availability(entry):
            """Convert blocked slots ("X") to integers."""
            if 'X' in entry:
                return 0
            else:
                return int(entry)
        # extract timetable and convert availability to integer:
        self.data["Verfuegbar"] =  [map(availability, line[1:]) for line in self.file_as_list[timetable_offset : timetable_offset + 4]] # first week
        self.data["Verfuegbar"] += [map(availability, line[1:]) for line in self.file_as_list[timetable_offset + 6 : timetable_offset + 10]] # second week
        
    def check_values(self):
        """
        Performs some tests on the data.
        """
        # Check that each field is filled:
        for key in self.data:
            if key != "Mobil" and self.data[key] is None:  # Only "Mobil" field is optional
                raise ValueError("Fehlender Eintrag:\t{}".format(key))
        
        # Check that values are in correct range:
        if not self.data["Monatsstunden"] in [40, 41, 60, 80]:
            raise ValueError("Ungültiger Eintrag:  {} Monatsstunden".format(self.data["Monatsstunden"]))
        
        if not self.data["C-Kenntnisse"] in range(4):
            raise ValueError("Ungültiger Eintrag:  C-Kenntnisse ist {}, sollte zwischen 0 und 3 liegen"\
                             .format(self.data["C-Kenntnisse"]))
        
        # uncertainty should be less than or equal to available slots in 2nd week 
        if not self.data["Unsicherheit"] <= number_of_nonzero_entries(self.data["Verfuegbar"][4:]):
            raise ValueError("Ungültiger Eintrag:  Mehr Unsicherheit ({}) als mögliche Termine ({}) in der 2. Woche"\
                             .format(self.data["Unsicherheit"], number_of_nonzero_entries(self.data["Verfuegbar"][4:])))
        
        # Check that availability scores are all there and in correct range:
        for line in self.data["Verfuegbar"]:
            if len(line) != 5:
                raise ValueError("Ungültige Zeile im Terminplan:  {}".format(" ".join(map(str, line))))
            for entry in line:
                if not entry in range(4):
                    raise ValueError("Ungültiger Eintrag:  Verfügbarkeitswert ist {}, sollte zwischen 0 und 3 liegen".format(entry))


def number_of_nonzero_entries(list_of_lists):
    """Returns the number of non-zero entries in a list of lists."""
    list_of_lists = [entry for sublist in list_of_lists for entry in sublist]  # flatten list
    return sum(1 for entry in list_of_lists if entry != 0)
    
if __name__ == "__main__":
    # find tutor files:
    import os
    files = ["../csv/tutoren/" + filename for filename in os.listdir("../csv/tutoren/") if filename.endswith(".csv")]
    
    max_word_width = max([len(word) for word in keys]) + 2  # Used for output formatting
    for filename in files:
        try:
            tutor = Tutor(filename)
            tutor.check_values()
            for key in keys:
                if key != "Verfuegbar":
                    print "".join([key.ljust(max_word_width), str(tutor.data[key])])
            print "Verfügbarkeitstabelle:"
            for line in tutor.data["Verfuegbar"]:
                print line
        except ValueError, e:
            print "Fehler bei Tutor {} {}:\n{}".format(tutor.data["Vorname"], tutor.data["Name"], e)
            print "Kontakt:"
            print tutor.data["E-Mail"]
            if not tutor.data["Mobil"] is None:
                print tutor.data["Mobil"]
        print "\n"

#!/usr/bin/python

# BGlog.py
# Derek Johnson
# 01 Apr 2013
#
# Description: Read Exported Glucose Buddy log and print table of BG values.
import sys
import csv
import datetime
from pprint import pprint

logfile = "/Users/derekjohnson/Dropbox/Diabetes/MyExportedGlucoseBuddyLogs.csv"

class BGreading(object):
    def __init__(self, reading):
        self.value = float(reading['Value'])
        self.datetime = reading['Date Time'] 
        self.event = reading['Event']
    def toString(self):
        return "%s: %2.1f" % (self.event, self.value)
    def getValue(self):
        return self.value
    def getDate(self):
        return self.datetime.date()
    def getEvent(self):
        return self.event
    def getTime(self):
        return self.datetime.time()
    def beforeNoon(self):
        noon = datetime.time(12, 0, 0)
        return (self.getTime() < noon)

def ReadGlucoseBuddyLogFile(logfilename):
    Readings = []
    try:
        f = open(logfilename)
        reader = csv.DictReader(f)
        for row in reader:
            row['Date Time'] = datetime.datetime.strptime(row['Date Time'], "%m/%d/%Y %H:%M:%S")
            Readings.append(row)
    finally:
        f.close()
    return Readings    

def GenerateBGReadings(Readings):
    BGreadings = {}

    for bgReading in [ BGreading(r) for r in Readings if r['Type'] == 'BG' ]:
        date = str(bgReading.getDate())
        BGreadings[date] = BGreadings.get(date, [])
        BGreadings[date].append(bgReading)

    return BGreadings

def GenerateDailyReadings(Readings):
    DailyReadings = {}

    for reading in Readings:
        date = str(reading['Date Time'].date())
        DailyReadings[date] = DailyReadings.get(date, [])
        DailyReadings[date].append(reading)

    return DailyReadings

def PrintBGReadingsCSV(BGreadings):

    event_order = ['Out Of Bed',
                   'During Night',
                   'Before Breakfast',
                   'After Breakfast',
                   'Before Lunch',
                   'After Lunch',
                   'Before Dinner',
                   'After Dinner',
                   'Before Bed']

    # Print the CSV file header
    print "Date,%s" % ','.join(event_order)
    
    dates = BGreadings.keys()
    dates.sort()
    for date in dates:
        events = {}
        for reading in BGreadings[date]:
            e = str(reading.getEvent())
            events[e] = events.get(e, [])
            events[e].append(str(reading.getValue()))
        
        line = []
        for e in event_order:
            line.append("|".join(events.get(e, '')))
        print "%s,%s" % (date, ','.join(line))

if __name__ == "__main__":
    Readings = ReadGlucoseBuddyLogFile(logfile)
    #pprint([ r for r in Readings if r['Type'] == 'BG' ])
    
    BGreadings = GenerateBGReadings(Readings)
    #pprint(BGreadings)

    DailyReadings = GenerateDailyReadings(Readings)
    #pprint(DailyReadings)

    PrintBGReadingsCSV(BGreadings)

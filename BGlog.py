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

def PrintHourlyBGReadingsCSV(BGreadings):
    # Print BG Readings on an hour by hour basis
    '''
    Output to CSV file.
    Open CSV file in Excel.

    Use the following conditional formatting rules to highlight weekends,
    hypos, good values and hyper:

    Cell value between 8.5 and 10  - yellow fill with yellow text
    Cell value between 4.1 and 8.5 - green fill with green text
    Cell value between 0.1 and 4.0 - red fill
    formula: weekday($a2,2)>5      - light grey fill
    '''

    hours = [ datetime.time(h, 0, 0) for h in xrange(24) ]

    print "Date,%s" % ','.join([ "%02d:00" % x.hour for x in hours ])
    dates = BGreadings.keys()
    dates.sort()
    for date in dates:
        hour_val = [ "" for x in xrange(24) ]
        for reading in BGreadings[date]:
            hour_val[ reading.getTime().hour ] = str(reading.getValue())
        
        print "%s,%s" % (date, ','.join(hour_val))

if __name__ == "__main__":
    Readings = ReadGlucoseBuddyLogFile(logfile)
    #pprint([ r for r in Readings if r['Type'] == 'BG' ])
    
    BGreadings = GenerateBGReadings(Readings)
    #pprint(BGreadings)

    DailyReadings = GenerateDailyReadings(Readings)
    #pprint(DailyReadings)

    PrintBGReadingsCSV(BGreadings)
    
    #PrintHourlyBGReadingsCSV(BGreadings)

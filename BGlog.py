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

logfile = open("/Users/derekjohnson/Dropbox/Diabetes/MyExportedGlucoseBuddyLogs.csv")

def extract_date(date_time = '03/14/2007 09:15:00'):
    '''Extract the date from the date-time string'''
    year = int(date_time[6:10])
    month = int(date_time[0:2])
    day = int(date_time[3:5])
    return datetime.date(year, month, day)

def extract_time(date_time = '03/14/2007 09:25:00'):
    '''Extract the date from the date-time string'''
    hour = int(date_time[11:13])
    minute = int(date_time[14:16])
    sec = int(date_time[17:19])
    return datetime.time(hour, minute, sec)

class BGreading(object):
    def __init__(self, value, date_time, event):
        self.value = float(value)
        self.date = extract_date(date_time)
        self.time = extract_time(date_time)
        self.event = event
    def toString(self):
        return "%s: %2.1f" % (self.event, self.value)
    def getValue(self):
        return self.value
    def getDate(self):
        return self.date
    def getEvent(self):
        return self.event
    def getTime(self):
        return self.time
    def beforeNoon(self):
        noon = datetime.time(12, 0, 0)
        return (self.time < noon)

if __name__ == "__main__":
    event_order = ['Out Of Bed',
                   'During Night',
                   'Before Breakfast',
                   'After Breakfast',
                   'Before Lunch',
                   'After Lunch',
                   'Before Dinner',
                   'After Dinner',
                   'Before Bed']
    BGreadings = {}
    Readings = []
    try:
        reader = csv.DictReader(logfile)
        for row in reader:
            Readings.append(row)
            if row['Type'] == 'BG':
                reading = BGreading(row['Value'], row['Date Time'], row['Event'])
                date = str(reading.getDate())
                BGreadings[date] = BGreadings.get(date, [])
                BGreadings[date].append(reading)
    finally:
        logfile.close()

    #pprint(BGreadings)
    #pprint(Readings)
    
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

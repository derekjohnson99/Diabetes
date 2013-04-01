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

class BGreading():
    def __init__(self, value, date_time, event):
        self.value = float(value)
        self.date = extract_date(date_time)
        self.time = extract_time(date_time)
        self.event = event
    def toString(self):
        return "%s: %s %2.1f [%s]" % (self.date, self.time, self.value, self.event)

if __name__ == "__main__":
    BGreadings = []
    try:
        reader = csv.DictReader(logfile)
        for row in reader:
            if row['Type'] == 'BG':
                BGreadings.append(BGreading(row['Value'], row['Date Time'], row['Event']))
                #print "%s %0.1f %s" % (row['Date Time'], float(row['Value']), row['Event'])
    finally:
        logfile.close()

for reading in BGreadings:
    print reading.toString()

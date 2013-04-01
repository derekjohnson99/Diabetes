#!/usr/bin/python

# BGlog.py
# Derek Johnson
# 01 Apr 2013 
#
# Description: Read Exported Glucose Buddy log and print table of BG values.
import sys
import csv
from pprint import pprint

logfile = open("/Users/derekjohnson/Dropbox/Diabetes/MyExportedGlucoseBuddyLogs.csv")

def extract_date(date_time = '03/14/2007 09:15:00'):
    '''Extract the date from the date-time string'''
    return date_time[:10]

def extract_time(date_time = '03/14/2007 09:25:00'):
    '''Extract the date from the date-time string'''
    return date_time[11:-3]

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

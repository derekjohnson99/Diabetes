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

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.lib.pagesizes import letter, A4, landscape, portrait

width, height = portrait(A4)

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

def GetCoordsFromDate(date_time):
    startOfDay = date_time.replace(hour=0, minute=0, second=0)
    x = ((date_time - startOfDay).seconds / 86400.0) * (width - 4.0) + 2.0
    y = height - (date_time.day * 26) - 19
    return (x, y)

def GenerateFortnightPDF(DailyReadings, start, pdf):

    # Draw a border
    pdf.line(2, 2, 2, height-2)
    pdf.line(2, height-2, width-2, height-2)
    pdf.line(width-2, 2, width-2, height-2)
    pdf.line(2, 2, width-2, 2)

    # Write header
    title = "Derek Johnson diabetes management %s" % (start.strftime("%d %B %Y"))
    pdf.setFont("Times-Roman", 18)
    pdf.drawCentredString(width/2.0, height-24, title)

    # Write key
    pdf.setStrokeColor(colors.lightgrey)
    pdf.line(40, 50, 130, 50)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 54, "BG (mmol/l)")
    pdf.drawString(50, 41, "Humalog (units)")

    # Write hour headings
    pdf.setFont("Helvetica", 12)
    hours = { 3: "3am", 6: "6am", 9: "9am", 12: "Noon", 15: "3pm", 18: "6pm", 21: "9pm"}
    for hour in hours.keys():
        pdf.drawCentredString((hour / 24.0) * (width - 4.0) + 2.0, height - 48, "%s" % hours[hour])

    x6 = (6.0 / 24.0) * (width - 4.0) + 2.0
    x12 = (12.0 / 24.0) * (width - 4.0) + 2.0
    x18 = (18.0 / 24.0) * (width - 4.0) + 2.0
    pdf.setStrokeColor(colors.lightgrey)
    [ pdf.line(x, 2, x, height - 72) for x in [x6, x12, x18] ] 
    
    # Write dates
    date = start
    current_line = height - 72
    for i in range(14):
        pdf.setFillColor(colors.lightgrey)
        pdf.line(2, current_line - 2, width-2, current_line - 2)
        pdf.setFont("Times-Roman", 18)
        pdf.drawString(0.2 * cm, current_line, date.strftime("%a %d/%m"))
        pdf.setFillColor(colors.black)
        pdf.setFont("Helvetica", 10)
        for reading in DailyReadings[str(date)]:
            c = GetCoordsFromDate(reading['Date Time'])
            if reading['Type'] == 'BG':
                pdf.drawCentredString(c[0], current_line + 1, "%s" % reading['Value'])
            if reading['Type'] == 'M' and reading['Name'] == 'Humalog':
                pdf.drawCentredString(c[0], current_line - 11, "%d" % int(float(reading['Value'])))
        date = date + datetime.timedelta(days=1)
        current_line = current_line - 52
    
    
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

    #PrintBGReadingsCSV(BGreadings)
    
    #PrintHourlyBGReadingsCSV(BGreadings)
    startdate = datetime.date.today() - datetime.timedelta(days=14)
    for i in range(1):
        pdf = Canvas("BG_Readings%s.pdf" % startdate.strftime("%d%b"), pagesize = portrait(A4))
        GenerateFortnightPDF(DailyReadings, startdate, pdf)
        pdf.showPage()
        pdf.save()
        startdate += + datetime.timedelta(days=14)

require("lattice")

# Clear all objects
rm( list = ls() )

# Read Glucose Buddy log file.
logfile = "~/Dropbox/Diabetes/MyExportedGlucoseBuddyLogs.csv"
log = read.csv(logfile)

# Convert date time string in log to POSIXct date-time format.
log$Date.Time = as.POSIXct(strptime(log$Date.Time, format="%m/%d/%Y %H:%M:%S"))

# Extract the different readings from the log.
BG       = log[log$Type=='BG',]
Humalog  = log[log$Type=='M' & log$Name=='Humalog',]
Lantus   = log[log$Type=='M' & log$Name=='Lantus',]
Activity = log[log$Type=='A',]

end = tail(BG$Date, 1)
start = end - 3600 * 24 * 27 # 4 weeks ago

Last4WeeksBG = BG[BG$Date>=start & BG$Date<=end,]

timeOfDay = as.POSIXct(strftime(Last4WeeksBG$Date, format="%H:%M:%S"), format="%H:%M:%S")

mealtimes=c(as.POSIXct("08:00", format="%H:%M"),
            as.POSIXct("12:00", format="%H:%M"),
            as.POSIXct("18:00", format="%H:%M"))

p = xyplot(Last4WeeksBG$Value ~ timeOfDay | format(as.Date(Last4WeeksBG$Date), "%m-%d %a"),
  pch=19, xlab="Time", ylab="BG value (mmol/l)", layout=c(7,4),
  main="Derek Johnson Daily BG levels for past 4 weeks", as.table=TRUE,
  panel = function(x, y, ...) {
    panel.abline(h=c(4,8), v=mealtimes, col='lightgrey', lty='dotted')
    #ltext(x=x, y=y, labels=Last4WeeksBG$Event, pos=4, offset=0.25, cex=0.7)
    panel.xyplot(x, y, ...)
  }  )
print(p)
#axis.POSIXct(1, at=seq(as.POSIXct("00:00", format="%H:%M"), as.POSIXct("23:00", format="%H:%M"), by="hour"),
#             format="%H")

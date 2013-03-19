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

# Get the date of the last entry
end = tail(BG$Date, 1)
# Get the start date as 27 days before the end date
start = end - 3600 * 24 * 27

# Curtail the BG readings to be between the start and end dates
BG = BG[BG$Date>=start & BG$Date<=end,]

# Add lines to each graph representing typical times for breakfast,
# lunch and tea (8am, noon and 6pm respectively).
mealtimes=lapply(c("8", "12", "18"), as.POSIXct, format="%H")

p = xyplot(Value ~ as.POSIXct(strftime(Date.Time, format="%H:%M"), format="%H:%M") |
  format(as.Date(Date.Time), "%m-%d %a"), data=BG,
  pch=19, xlab="Time", ylab="BG value (mmol/l)", layout=c(7,4),
  main="Derek Johnson Daily BG levels for previous 28 days", as.table=TRUE,
  panel = function(x, y, ...) {
    panel.abline(h=c(4,8), v=mealtimes, col='lightgrey', lty='dotted')
    #ltext(x=x, y=y, labels=BG$Event, pos=4, offset=0.25, cex=0.7)
    panel.xyplot(x, y, ...)
  }  )
print(p)
#axis.POSIXct(1, at=seq(as.POSIXct("00:00", format="%H:%M"), as.POSIXct("23:00", format="%H:%M"), by="hour"),
#             format="%H")

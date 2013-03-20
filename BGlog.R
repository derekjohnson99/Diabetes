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

# Use the date part of the Date.Time as the conditioning variable for the xyplot
Day = format(as.Date(BG$Date.Time), "%A %d %B")

# The xyplot function will factor the date automatically, but will
# sort it alphabetically, so we need to factor it manually and ensure
# it is sorted chronologically.
Day = factor(Day, levels = unique(Day))

p = xyplot(Value ~ as.POSIXct(strftime(Date.Time, format="%H:%M"), format="%H:%M") |
  Day, data=BG, scales=list(x=list( format="%I%p" ), y=list(at=c(4,8,12,16))),
  pch=19, xlab="Time", ylab="BG value (mmol/l)", layout=c(7,4), as.table=TRUE,
  main=list(label="Derek Johnson Daily BG levels for previous 28 days", cex=0.75),
  panel = function(x, y, ...) {
    panel.abline(h=c(4,8), v=mealtimes, col='lightgrey', lty='dotted')
    panel.xyplot(x, y, ...)
  }  )

print(p)

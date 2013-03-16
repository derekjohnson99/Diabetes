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

# Function to plot a given day's BG values
## plotDay = function(date)
## {
##   S = date
##   E = date + 3600 * 24
##   h6 = 3600 * 6
##   tcks = c(S, S+h6, S+h6*2, S+h6*3, S+h6*4)
##   plot(BG$Date[BG$Date>=S & BG$Date<E], BG$Value[BG$Date>=S & BG$Date<E],
##        xlim = c(S, E), ylim=c(0,20), xlab=format(S, "%a %b %d"), ylab="BG (mmol/l)", xaxt="n")
##   axis.POSIXct(1, at=tcks)
##   abline(h=4, lty=3)
##   abline(h=8, lty=3)
## }

## par(mfrow=c(4,7), pch = 19)

## start = as.POSIXct("2013-02-13")
## for (i in seq(28))
## {
##   plotDay(start)
##   start = start + 3600 * 24
## }

end = Sys.time()
start = end - 3600 * 24 * 28 # 4 weeks ago

Last4WeeksBG = BG[BG$Date>start & BG$Date<end,]

timeOfDay = as.POSIXct(strftime(Last4WeeksBG$Date, format="%H:%M:%S"), format="%H:%M:%S")

mealtimes=c(as.POSIXct("08:00", format="%H:%M"),
            as.POSIXct("12:00", format="%H:%M"),
            as.POSIXct("18:00", format="%H:%M"))

print(mealtimes)

p = xyplot(Last4WeeksBG$Value ~ timeOfDay | as.Date(Last4WeeksBG$Date),
  pch=19, xlab="Time", ylab="BG value (mmol/l)",
  main="Derek Johnson Daily BG levels for past 4 weeks", as.table=TRUE,
  panel = function(...) {
    panel.abline(h=c(4,8), v=mealtimes, col='lightgrey', lty='dotted')

    panel.xyplot(...)
  }
  )

print(p)

library(lattice)
library(grid)
library(chron)

source("https://raw.githubusercontent.com/iascchen/VisHealth/master/R/calendarHeat.R")

library(httr)
cat(content(GET("https://raw.githubusercontent.com/iascchen/VisHealth/master/R/calendarHeat.R"), "text"), file="calendarHeat.R")
source("calendarHeat.R")

data <- read.csv('~/Desktop/projects/gym_data/all.csv', header = TRUE, sep = ',')
head(data)
data$Date <- as.POSIXct(strptime(data$Date, format = "%Y-%m-%d"), varname = data$Time)
head(df)
#calendarHeat(Date, Time, ncolors = 99, color = "r2b", varname = "Values", date.form = "%Y-%m-%d")
calendarHeat(dates = data$Date, values = data$Time, color = "r2b", varname = "Time", ncolors=99)
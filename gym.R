#Data Converter
library(magrittr)
library(dplyr)
library(tidyr)

df <- read.csv("~/Desktop/projects/gym_data/2018.csv",header = TRUE, sep=",",quote="\"")
split_1 <- df %>% separate(X, c("Date", "Time"), sep=" ")
date <- data.frame(split_1[8:154 ,c(2)])
names(date)[1] = 'Date'
split_2 <- split_1 %>% separate(Date, c("Month", "Day", "Year"), sep="/")
combine <- split_2[8:154,c(2,3,4,5)]
# -1 last row and -1 first row indexing
gym_data <- bind_cols(date, combine)

write.csv(gym_data, file = "~/Desktop/projects/gym_data/2018_split.csv")
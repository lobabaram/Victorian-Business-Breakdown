install.packages('dplyr')
install.packages('rvest')
install.packages("ggplot2")
install.packages('tidyr')
install.packages('tidyverse')
install.packages('ggthemes')
install.packages('gridExtra')
install.packages('tabulizer')
install.packages('GGally')
install.packages("rjson") # Optional
install.packages("readr")
install.packages("ggmap")
install.packages("leaflet")
install.packages("sf")
install.packages("geojsonio")

# Load the geojsonio library
library(geojsonio)
library(jsonlite)

library(leaflet)
library(ggmap)
library(rjson)
library(GGally)
library(readxl)
library(tabulizer)
library(dplyr)
library(rvest)
library(ggplot2)
library(tidyr)
library(lubridate)
library(ggthemes)
library(gridExtra)
library(scales)
library(readr)
library(sf)



# # Give the input file name to the function.
# df <- fromJSON(file = "vicdata.json")
# 
# # Print the result.
# print(df)
# 
# json_df <- as.data.frame(df)
# 
# print(json_df)

# asicdata <- read.csv("company_202310.csv", header = TRUE,sep = "/t")

# asicdata <- read_delim("company_202310.csv",delim = "\t", escape_double = FALSE, trim_ws = TRUE)
# View(asicdata)

pecdata <- read_delim("counts-of-australian-businesses-by-lga.csv", 
                         delim = ";", escape_double = FALSE, trim_ws = TRUE)

# pecdata <- read.csv("counts-of-australian-businesses-by-lga.csv", header = TRUE, sep = ";")

glimpse(pecdata)

# Create Factors
unique(pecdata$State)
unique(pecdata$`Industry Code`)
unique(pecdata$`Industry Label`)
unique(pecdata$METRO)

pecdata$State <- as.factor(pecdata$State)
pecdata$`Industry Code` <- as.factor(pecdata$`Industry Code`)
pecdata$`Industry Label`<- as.factor(pecdata$`Industry Label`)
pecdata$METRO <- as.factor(pecdata$METRO)

# Filter Our Victoria and Total 
vdata <- c("Victoria","Total Victoria")

pecdata %>% select(State) %>%  filter(State == "Victoria" ) %>% table()

pecdata %>% select(State) %>%  filter(State %in% vdata ) %>% table()

vicdata <- pecdata %>% filter(State %in% vdata)

totalvic <- vicdata %>% filter(vdata[2]== State)

vicdata <- vicdata %>% filter(!State %in% totalvic$State)

# Clean Missing Values
vicdata <-vicdata  %>%  filter(is.na(vicdata$LGA) == FALSE)

vicdata %>% filter(is.na(`LGA Label`)) %>% count()
vicdata %>% filter(is.na(`Industry Code`)) %>% count()
vicdata %>% filter(is.na(`Industry Label`)) %>% count()
vicdata %>% filter(is.na(`Non employing`)) %>% count()

vicdata %>% filter(is.na(`1-4 Employees`)) %>% count()
vicdata %>% filter(is.na(`5-19 Employees`)) %>% count()
vicdata %>% filter(is.na(`20-199 Employees`)) %>% count()
vicdata %>% filter(is.na(`200+ Employees`)) %>% count()

names(which(colSums(is.na(vicdata)) > 0))

# Area / Population / Joint Regional Groups / Metro / Other Groups / Geom / Centroid

# data that shows no area has no meaning because it doesn't have an address for us to map
# Area
narows <- vicdata[is.na(vicdata$AREA),]

names(which(colSums(is.na(narows)) > 0 ))

# Remove data in vicdata from narows

vicdata <- vicdata %>% filter(!LGA %in% narows$LGA)

# Population 
narows <- vicdata %>% filter(POPULATION <=0)

# Join Regional Groups
narows <- vicdata[is.na(vicdata$`Joint / Regional Groups`),]

names(which(colSums(is.na(vicdata)) > 0))

which(colSums(is.na(vicdata)) > 0)

sum(is.na(vicdata$AREA))

which(is.na(vicdata))


# Seperate Centroid into Longitude and Latitude
head(vicdata$geom)
vicdata$centroid[1]

vicdata <- vicdata %>% separate(centroid, into = c("Latitude","Longitude"),sep = ",")

################################################################################################################
# Testing geom 
jdata <- head(vicdata$geom[1])
print(jdata)

class(vicdata$geom)


cat(jdata)
# Remove the second pair of quotes
cleaned_data <- gsub('""', '"', jdata)
cat(cleaned_data, "\n")
print(cleaned_data)
class(cleaned_data)

# Load the JSON string as a JSON object
json_obj <- jsonlite::fromJSON(cleaned_data, simplifyVector = FALSE)


# APPLYING IT TO ENTIRE COLUMN
vicdata2 <- vicdata
cat(vicdata2$geom[1])

# Apply gsub to clean the column
vicdata2$geom <- lapply(vicdata2$geom, function(x) gsub('""', '"', x))

# Convert the list back to a character vector
vicdata2$geom <- sapply(vicdata2$geom, function(x) paste(x, collapse = ""))

# Print the cleaned data
cat(vicdata2$geom[1][1][1])
class(vicdata2$geom)


vicdata <- vicdata2

##################################################################################
# Make sure every state has every single industry type and set them to 0 because there is no data in them

write.csv(vicdata, "C:\\Anthony\\Work\\Cleanly Data Analysis\\Coding Folder\\vicdata.csv", row.names=FALSE)

cat(vicdata2$geom)
head(vicdata2$geom)







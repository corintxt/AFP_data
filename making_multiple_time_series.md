---
title: "Making a chart with multiple time series lines from long data in R"
author: "Corin Faife"
date: "October 16, 2023"
output:
  md_document:
    variant: markdown_github
---
# Making a chart with multiple time series lines from long data in R
## Context

-   We have some time series data in “long” format, i.e. one row for
    each time observation on each day over multiple years.
-   We want to make a chart that plots multiple years superimposed.
-   Ideally we don’t want to mutate the data by adding new columns, fake
    data, etc.

### Downloading the data

First we load libraries we’ll need to manipulate the data. (If you don’t
have them they’ll need to be installed first with
`install.package('packagename')`)

``` r
library(ggplot2)
library(lubridate)
library(zoo)
```

For this chart, we’re going to be using data showing the height of the
Mississippi River at Memphis Tennessee.

To obtain this data we first load the US Geological Survey’s [data
retrieval R package](https://waterdata.usgs.gov/blog/dataretrieval/).

``` r
library(dataRetrieval)
```

The documentation for the `dataRetrieval` package suggests we will need
to use the function `readNWISdv()` to get daily values from the National
Water Information System.

Let’s look at the help page for the function to get some information on
usage.

``` r
?readNWISdv
```

    Description
    Imports data from NWIS web service. This function gets the data from here: https://waterservices.usgs.gov/

    Usage
    readNWISdv(
      siteNumbers,
      parameterCd,
      startDate = "",
      endDate = "",
      statCd = "00003"
    )

So, we need to get the site number and parameter code. The [page for the
Memphis, Tennessee monitoring
location](https://waterdata.usgs.gov/monitoring-location/07032000/#parameterCode=00065&period=P3400D&showMedian=true)
gives us a unique identifying number for the site: `07032000`.

The USGS data on river height is measured by a displacement gage. USGS
lists many different [parameter
codes](https://help.waterdata.usgs.gov/parameter_cd?group_cd=PHY) on
their web, and the code for gage height is `00065`.

With this information we can make a request to the NWIS web service, and
assign the resulting dataframe to a variable:

``` r
data <- readNWISuv(siteNumbers = "07032000", # Memphis TN
                     parameterCd = "00065", # gage height
                     startDate = "2014-9-30", # earliest date we have data for
                     endDate = "")
```

The USGS package also has a built in function, `renameNWISColumns()`,
that will rename columns in datasets pulled from the NWIS system to have
more human-readable names.

We can then call the `head()` function to see the first few rows of the
data frame.

``` r
data <- renameNWISColumns(data)
head(data)
```

    ##   agency_cd  site_no            dateTime GH_Inst GH_Inst_cd tz_cd
    ## 1      USGS 07032000 2014-09-30 11:00:00    3.31          A   UTC
    ## 2      USGS 07032000 2014-09-30 12:00:00    3.27          A   UTC
    ## 3      USGS 07032000 2014-09-30 13:00:00    3.24          A   UTC
    ## 4      USGS 07032000 2014-09-30 14:00:00    3.21          A   UTC
    ## 5      USGS 07032000 2014-09-30 15:00:00    3.18          A   UTC
    ## 6      USGS 07032000 2014-09-30 16:00:00    3.17          A   UTC

### Charting the data

We now have all the data we need to make a line chart of river height
over time.

The USGS [blog](https://waterdata.usgs.gov/blog/dataretrieval/) has a
simple example of how to make a chart of data pulled from NWIS, so let’s
try it out, and plot the `GH_Inst` variable (gage height).

``` r
ggplot(data = data, aes(x = dateTime,
                        y = GH_Inst)) +
  geom_line()
```

![](images/figure-markdown_github/unnamed-chunk-6-1.png)

Our chart looks consistent for what we expect from seasonal variations
in the height of the river, and also shows that in 2022 and 2023 there
has been a dip in river levels beyond previous variations.

To make it clearer, what we want is to have an x axis that spans a
single year, and plot a separate line for each year of data instead of a
single line for all years. To do this, we’ll call two different
functions on the `dateTime` column as we plot the data.

The first, `yday()` from the
[`lubridate`](https://lubridate.tidyverse.org/) library, takes a date as
input and converts it to a day of the year from 1 to 365. The second,
`year()`, extracts only the year from a date.

On the x axis we’ll plot the `yday` of each data point, which means all
values will fall between day 1 and day 365 of a single year.

We will also *group* the data using the `year()` function and R’s
`factor()` operation, which [classifies a variable into
categories](https://www.learnbyexample.org/r-factor/):

``` r
ggplot(data, aes(x = yday(dateTime),
                 y = GH_Inst,
                 group = factor(year(dateTime)))) +
  geom_line()
```

![](images/figure-markdown_github/unnamed-chunk-7-1.png)

This is starting to get closer to what we want. To make things look
better, let’s also set line colour by group, and add some labels.

``` r
ggplot(data, aes(x = yday(dateTime),
                 y = GH_Inst,
                 group = factor(year(dateTime)),
                 colour = factor(year(dateTime)))) +
  geom_line() +
  labs(x = "Month",
       y = "Water height", 
       colour = "Year",
       title = "Mississippi River Height at Memphis, TN")
```

![](images/figure-markdown_github/unnamed-chunk-8-1.png)

This is much better, but there are still two things we need to fix for
the finished chart.

Firstly, we want the x axis to be labelled with the months of the year
rather than the 1-365 `yearday` number. We can do this with an R
function [called
`scale_x_date()`](https://ggplot2.tidyverse.org/reference/scale_date.html),
which takes arguments for where to put chart ticks for
hours/days/weeks/months and where to put labels on the x axis.

To use this function, we will also need to use another function,
`as.Date()`, on the mapping of the x variable, so that `scale_x_date`
can understand it as a date instead of the yearday number.

``` r
ggplot(data, aes(
                x = as.Date(yday(dateTime)),
                y = GH_Inst, 
                group=factor(year(dateTime)), 
                colour=factor(year(dateTime)))) +
  geom_line() +
  labs(x = "Month", 
  y = "Water height", 
  colour = "Year",
  title = "Mississippi River Height at Memphis, TN") +
  scale_x_date(date_breaks = "2 month", date_labels = "%b")
```

![](images/figure-markdown_github/unnamed-chunk-9-1.png)

### Calculating daily means

At the moment our chart shows a series of steps instead of a smooth
line. This is because we are plotting multiple observations for each day
on the chart (the hourly gage readings), whereas it would be better to
just plot a single data point for each day.

This means we need to aggregate the data by day and calculate a single
mean value for each day. First we’ll create a new column that extracts
just the date from the `dateTime` column, in year-month-day format.

``` r
data$date <- format(as.Date(data$dateTime), "%Y-%m-%d")
```

Then, we’ll use R’s `aggregate` function to calculate a mean value. The
[documentation](https://r-coder.com/aggregate-r/) for the function tells
us that the function takes an input object, a list of variables to group
by, and a function to be applied if calculating summary statistics for
the group.

In our case, the input is the `GH_Inst` column, the variables to group
by are the dates in our new `date` column, and the function is a mean
average. We’ll assign the result to a new variable called `dailydata`,
and rename the columns (otherwise they would have default names that are
not descriptive of the data).

``` r
dailydata <- aggregate(data$GH_Inst, list(data$date), FUN=mean)

names(dailydata)[1] <- "date"
names(dailydata)[2] <- "gage_height"
```

Now we can remake the chart using our new dataframe:

``` r
ggplot(dailydata, aes(
                x = as.Date(yday(date)),
                y = gage_height, 
                group=factor(year(date)), 
                colour=factor(year(date)))) +
  geom_line() +
  labs(x = "Month", 
  y = "Water height", 
  colour = "Year",
  title = "Mississippi River Height at Memphis, TN") +
  scale_x_date(date_breaks = "2 month", date_labels = "%b")
```

![](images/figure-markdown_github/unnamed-chunk-12-1.png)

The chart now displays the data as we want it, and is ready to export to
an SVG to finalize in Illustrator.

``` r
ggsave("Memphis_river_daily_data.svg")
```

    ## Saving 7 x 5 in image

------------------------------------------------------------------------

## Complete code:

``` r
# Load libraries we'll need
library(dataRetrieval)
library(ggplot2)
library(lubridate) # needed for yday function
library(zoo)

# Load the data
data <- readNWISuv(siteNumbers = "07032000",
                     parameterCd = "00065",
                     startDate = "2014-9-30",
                     endDate = "")
# Rename columns
data <- renameNWISColumns(data)
# Make a date column
data$date <- format(as.Date(data$dateTime), "%Y-%m-%d")
# Find daily mean
dailydata <- aggregate(data$GH_Inst, list(data$date), FUN=mean)
# Rename columns
names(dailydata)[1] <- "date"
names(dailydata)[2] <- "gage_height"
# Plot
riverchart = ggplot(dailydata, aes(
                x = as.Date(yday(date)),
                y = gage_height, 
                group=factor(year(date)), 
                colour=factor(year(date))
                )) +
                geom_line() +
                labs(x = "Month", 
                    y = "Water height", 
                    colour = "Year",
                    title = "Mississippi River Height at Memphis, TN") +
                scale_x_date(date_breaks = "2 month", date_labels = "%b")

# Save
ggsave("MemphisTN_river_daily_data.svg")
```

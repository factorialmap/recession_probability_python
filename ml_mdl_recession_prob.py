
#packages
from fredapi import Fred
import numpy as np
import pandas as pd

#insert api_key from fred
fred = Fred(api_key='insert api_key')

#get 10y data as pandas series freq = montly
data_t10y3m = fred.get_series("T10Y3M", frequency = "m")

#transform pandas series into data frame with y_name = 10y3m
data_t10y3m = data_t10y3m.to_frame(name = '10y3m')

#rename index to date
data_t10y3m = data_t10y3m.rename_axis("date")

#check results
data_t10y3m.head(3)

#get usrec data as panda series freq = montly
data_usrec = fred.get_series("USREC", frequency = "m")

#transform pandas series into data frame with y_name = recession
data_usrec = data_usrec.to_frame(name = 'recession')

#rename index to date
data_usrec = data_usrec.rename_axis("date")

#check results
data_t10y3m.head(3)
data_usrec.head(3)

#merge df including three columns date, 10y3m, recession
data_rec = data_t10y3m.merge(
    data_usrec, 
    left_on = "date", 
    right_on = "date")

#save data into csv file
data_rec.to_csv("data_rec.csv")


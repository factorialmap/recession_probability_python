
#packages
from fredapi import Fred
import numpy as np
import pandas as pd

#api key
fred = Fred(api_key="insert api key")

#get 10y data
data_t10y3m = fred.get_series("T10Y3M", frequency = "m")

#save 10y data
data_t10y3m.to_csv("data_t10y3m.csv")

#get usrec data
data_usrec = fred.get_series("USREC", frequency = "m")

#save usrec data
data_usrec.to_csv("data_usrec.csv")

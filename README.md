####  Exercise with simple recession probability model using two variables USREC and T10Y3M with python code

There is a market behavior that believes that at each turn in the yield curve, which is the difference between 10-year bonds vs 3-months treasury bills, the probability of recession increases. 
Histsorically, we have only four observations describing this phenomenon, which makes it very fragile to establish a cause-and-effect relationship, however, considering that the economy as a social phenomenon, 
we decided to make a machine learning model with the following goals:

- Better understand the phenomenon by colleting information as it happens
- Collet data from the FED using Python API
- Create machine learning models using python code.
- Create probability model production web interface

![image](https://github.com/user-attachments/assets/998908e1-c8a9-4087-95e1-982afae8872c)


The objective of this exercise is not to make market decisions, but to better understand the phenomenon and practice critical thinking about tools for collecting, pre-processing, developing, and publishing 
machine learnig models using in a python environment.


#### What is USREC?

- USREC is an interpretation of US business cycle expansions and contractions data provided by The National Bureau of Economic Research(NBER). Where 0 = not recession and 1 = recession.

Source: Federal Reserve Bank of St. Louis, NBER based Recession Indicators for the United States from the Period following the Peak through the Trough [USREC], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/USREC, August 5, 2024. 

#### What is 10Y3M?

- T10Y3M represents the spread between 10-Year Treasury Constant Maturity and 3-Month Treasury Constant Maturity. When the value is positive, it means that the interest rate paid for the three-month t-bill is lower than the interest rate paid for the 10-year bond.

Source: Federal Reserve Bank of St. Louis, 10-Year Treasury Constant Maturity Minus 3-Month Treasury Constant Maturity [T10Y3M], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/T10Y3M, August 5, 2024. 


#### How to get data?

- The data is provided by the Federal Reserve Bank of St. Louis and the `freadapi` library will be used to obtain it.

- The library installation process is available at: https://pypi.org/project/fredapi/

- An API key is required and can be created when logging into FRED.
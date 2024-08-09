
#packages
from fredapi import Fred
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

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


#split data into a training and testing sets
X = data_rec[["10y3m"]]
y = data_rec[["recession"]]

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, 
random_state=42)

#create a logistic regression model
mdl_log_reg_rec = LogisticRegression()

#train the model in the training data
mdl_log_reg_rec.fit(X_train, y_train)

#make predictions on the testing data
y_pred = mdl_log_reg_rec.predict(X_test)

#evaluate the model
accuracy = accuracy_score(y_test, y_pred)
accuracy

print("Accuracy:", accuracy)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))


#predict new data
new_data = pd.DataFrame({"10y3m":[1,0.5,-0.5]})

new_pred = mdl_log_reg_rec.predict(new_data)
new_pred

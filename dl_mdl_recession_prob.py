#create a model using pytorch

import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

#data frame 
data_rec.head(3)

#split the data into training and testing set
X = data_rec[["10y3m"]].values
y = data_rec[["recession"]].values

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size =0.2,
random_state=42)

#convert data to pytorch tensors
X_train = torch.from_numpy(X_train).float()
X_test = torch.from_numpy(X_test).float()
y_train = torch.from_numpy(y_train).long()
y_test = torch.from_numpy(y_test).long()

#neural network mdl specification

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(1,10) #1 input layers to 10 hidden layers
        self.fc2 = nn.Linear(10,2) #10 hidden layers to 2 output layers
    def forward(self,x):
        x = torch.relu(self.fc1(x)) #activation function for hidden layer
        x = self.fc2(x)
        return x

#initialize the model, loss function, and optimizer
model = Net()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr = 0.001)

#train the model
for epoch in range(100):
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()
    if (epoch+1) % 10 == 0:
        print (f'Epoch [{epoch+1}/100], Loss: {loss



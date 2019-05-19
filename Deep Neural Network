#Import Libraries
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import os # to change directory
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.utils import to_categorical, np_utils
from keras.callbacks import EarlyStopping
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score, KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split,KFold,cross_val_score
from sklearn.preprocessing import MinMaxScaler
from keras import optimizers
from keras import regularizers, initializers
from keras.regularizers import l1,l2
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_squared_error
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
import math

os.chdir("D:/MOA Data")

#Importing data
df = pd.read_csv('consolidated_df_v9.csv')
df['Total_Revenue_2'] = df['Pseudo Rides Revenue']+ df['Food Revenue'] + df['Items Revenue']
df1 = df.drop(columns = ['Date', 'Total Revenue', 'Rides Revenue', 'Food Revenue', 
                         'Items Revenue','WB Pseudo Revenue', 'Points Pseudo Revenue',
                         'Pseudo Rides Revenue','Total Pseudo Revenue',
                         'Actual_Ridership','Efficiency','Modified Ridership',
                         'Total_Revenue_2', 'Unnamed: 0', 'Unnamed: 0.1',])
y = df['Total_Revenue_2']

#Ensure you have all columns
df1.columns

# splitting of dataset into training and testing
x_train, x_test, y_train, y_test = train_test_split(df1,y, test_size = 0.2,
                                                    random_state = 42, stratify = df['Shift'])

#Normalizing the variables
scaler = MinMaxScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

Y_train_temp = y_train.values
y_train = pd.DataFrame(Y_train_temp)
y.columns = ['Psuedo_Revenue']
Y_test_temp = y_test.values
y_test = pd.DataFrame(Y_test_temp)
y_test.columns = ['Pseudo_Revenue']

model = Sequential()
model.add(Dense(2500, activation= 'relu', 
                input_shape=(x_train.shape[1],), 
                kernel_regularizer=regularizers.l2(0.01)))
model.add(Dropout(0.2))
model.add(Dense(2500, activation='relu', 
                kernel_regularizer=regularizers.l2(0.01)))
model.add(Dropout(0.2))
model.add(Dense(2000, activation='relu', 
                kernel_regularizer=regularizers.l2(0.01)))
model.add(Dropout(0.2))
model.add(Dense(2000, activation='relu',
                kernel_regularizer=regularizers.l2(0.01)))
model.add(Dropout(0.2))
model.add(Dense(1, activation='linear',kernel_initializer='zero',activity_regularizer=regularizers.l1(0.01)))

adam = optimizers.adam(lr= 0.001, beta_1=0.9, beta_2=0.999,epsilon=None,decay = 0.001)
model.compile(optimizer= adam,loss='mean_squared_error', metrics=['mean_squared_error'])

#Model
early_stopping_monitor = EarlyStopping(patience=3)
model.fit(x_train_scaled, y_train, batch_size = 600, epochs = 500, callbacks=[early_stopping_monitor])

#Predict- training error
train_y_predictions = model.predict(x_train_scaled)
r_2_train = r2_score(y_train, train_y_predictions)
r_2_train
rmse_train = math.sqrt(mean_squared_error(y_train, train_y_predictions))
rmse_train

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

MAPE_train = mean_absolute_percentage_error(y_train, train_y_predictions)
MAPE_train

#Predict- testing error
test_y_predictions = model.predict(x_test_scaled)
r_2_test = r2_score(y_test, test_y_predictions)
r_2_test
rmse_test = math.sqrt(mean_squared_error(y_test, test_y_predictions))
rmse_test
MAPE_test = mean_absolute_percentage_error(y_test, test_y_predictions)
MAPE_test

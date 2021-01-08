#https://medium.com/towards-artificial-intelligence/beginners-guide-to-timeseries-forecasting-with-lstms-using-tensorflow-and-keras-364ea291909b

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, SimpleRNN
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator  # Generates batches for sequence data

x = np.linspace(0, 50, 501)
y = np.sin(x)
plt.plot(x,y)
# Define a dataframe using x and y values.

df = pd.DataFrame(data=y,index=x,columns=['Sine'])
plt.show()
print(df.to_string)

test_percent = 0.2
test_point = np.round(len(df) * test_percent)
test_index = int(len(df) - test_point)
train = df.iloc[:test_index]
test = df.iloc[test_index:]

scaler = MinMaxScaler()
scaler.fit(train)
MinMaxScaler(copy=True, feature_range=(0, 1))
scaled_train = scaler.transform(train)
scaled_test = scaler.transform(test)

length = 50
batch_size = 1
generator = TimeseriesGenerator(scaled_train, scaled_train, length=length, batch_size=batch_size)
print(len(scaled_train))
print(len(generator))

n_features = 1
model = Sequential()
model.add(SimpleRNN(50,input_shape = (length , n_features)))
model.add(Dense(1))
model.compile(optimizer='adam',loss='mse',metrics = ['accuracy'])
model.fit_generator(generator=generator,epochs=50)

first_eval_batch = scaled_train[-length:] # Take the last 50 points and predict the new value in the scaled_test
first_eval_batch = first_eval_batch.reshape((1,length,n_features)) # shape the data to match the input_shape of model
model.predict(first_eval_batch)# array([[0.92780817]], dtype=float32)
scaled_test[0] # array([0.94955134])




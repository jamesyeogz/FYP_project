import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from sklearn.preprocessing import StandardScaler,MinMaxScaler
import yfinance as yf 
import sys,pathlib
import pandas as pd
import datetime

def convertDatatoPredictModel(data,training_period):
  print(f'The data will have {data.shape[1]} features with {data.shape[0]} in quantity')
  X_data = []
  x = data[len(data)-training_period:len(data)]
  X_data.append(x)
  X = np.array(X_data)
  # X = tf.cast(X , dtype=tf.float32)
  # Y = tf.cast(Y , dtype=tf.float32)
  return X
def CleanupData(data, columns=['Dividends','Stock Splits','Capital Gains']):
  data = data.drop(columns=columns)
  return data
def ConvertDatatoScalarSimple(data):
  scalar = MinMaxScaler()
  data = scalar.fit_transform(data)
  return data, scalar
def Inverse_transform_Simple(Y_predict,scalar,features=5):
    Y_predict = Y_predict.reshape(-1,1)
    Y_predict = np.repeat(Y_predict,features,axis=-1)
    predicted = scalar.inverse_transform(Y_predict)[:,0]
    return predicted
def GetResults2Days(data,return_last=False):
    
    models ={
        2: 'ThursdayFriday',
        1: 'WednesdayThursday',
        0: 'TuesdayWednesday',
        4: 'MondayTuesday'
    }
    # Check if last 3 days is consistent with each other

    latest = data.iloc[-1]
    date_range_start = pd.to_datetime(latest.name) + datetime.timedelta(days=1 if latest.name.dayofweek != 4 else 3)
    date_range_end = date_range_start+datetime.timedelta(days=1)
    date_range = (date_range_start.strftime('%Y-%m-%d'),date_range_end.strftime('%Y-%m-%d'))
    if latest.name.dayofweek in models:
      model = models[latest.name.dayofweek]
      scriptpath = pathlib.Path(__file__).parent.resolve()
      scriptpath = f'{scriptpath}/models/model{model}.h5'
      model = load_model(scriptpath,compile=False)
      model.compile()
      data = CleanupData(data=data,columns=['Adj Close'])
      new_data,scalar = ConvertDatatoScalarSimple(data=data)
      new_data = convertDatatoPredictModel(data=new_data,training_period=3)
      prediction= model.predict(new_data)
      df = pd.DataFrame(pd.date_range(start=date_range[0], end=date_range[1]), columns=['Date'])
      predicted = Inverse_transform_Simple(prediction,scalar=scalar)
      predicted.reshape(-1,1)
      df['Predicted_Close'] = predicted.tolist()
      df.set_index("Date",inplace=True)
      data = pd.concat([data,df],axis='columns')
      data['signal'] = 0.0
      # We will do it manually since its the latest ones
      previous_index = None
      for index, row in data.iterrows():
        if not previous_index:
          previous_index = index
          continue
        previous = data.loc[previous_index]
        if not pd.isna(row.Predicted_Close):
          if not pd.isna(previous.Close):
            if previous.Close < row.Predicted_Close:
              data.loc[previous_index,['signal']] += 1
            else:
              data.loc[previous_index,['signal']] -= 1
          else:
            if previous.Predicted_Close < row.Predicted_Close:
              data.loc[previous_index,['signal']] += 0.5
            else:
              data.loc[previous_index,['signal']] -= 0.5
        previous_index=index
      # return data.iloc[4:len(data)-1]
      # return data.iloc[3:]
      return data
    else:
       return pd.DataFrame()
    

    


    # result = model.predict(new_data)



# data = yf.download(tickers='SPY', period='5d',interval='1d')
# data = data.iloc[2:]
# print(GetResults2Days(data))
import pandas as pd
import numpy as np
import yfinance as yf

def GetSMA(data,count=5,return_last=False):
    # data = yf.download(tickers='SPY', period='1y',interval='1d')    
    data['signal'] = 0.0
    data['RollingMax'] = (data.Close.shift(1).rolling(count).max())
    data['RollingMin'] = (data.Close.shift(1).rolling(count).min())
    data.loc[data['RollingMax'] < data.Close, 'signal'] = -1
    data.loc[data['RollingMin'] > data.Close, 'signal'] = 1
    data = data[data['RollingMax'].notna()]
    if not return_last:
        return data
    else:
        return data.tail(1)

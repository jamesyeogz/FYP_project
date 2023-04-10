import pandas as pd
import numpy as np
import yfinance as yf


def CandleStickPattern(ticker="SPY",min_candle_size=2):
    data = yf.download(tickers=ticker, period='1y', interval='1d')
    data['Candle_Body'] = abs(data['High']-data['Low'])
    data['Shift'] = 0
    data['signal'] = 0
    data.loc[(data['Candle_Body'] > min_candle_size) & (data['Open'] > data['Close']),'Shift'] = 1
    data.loc[(data['Candle_Body'] > min_candle_size) & (data['Open'] < data['Close']), 'Shift'] = -1
    for index,row in data.iterrows():
        loc = data.index.get_loc(index)
        if loc < 1:
            continue
        previous_data = data.iloc[loc-1]
        # print(previous_data)
        if row.Shift == 1 and previous_data['Shift'] == -1:
            data.loc[index,'signal'] = -1
        elif row.Shift == -1 and previous_data['Shift'] == 1:
            data.loc[index,'signal'] = -1
    return data

def EMAPatterns(ticker='SPY',short_EMA=5,med_EMA=30,long_ema=180):
    data = yf.download(tickers=ticker, period='1y', interval='1d')
    data = pd.DataFrame(data)
    data['short_EWM'] =  data['Close'].ewm(span=short_EMA, adjust=False).mean()
    data['med_EWM'] = data['Close'].ewm(span=med_EMA, adjust=False).mean()
    data['long_EWM'] = data['Close'].ewm(span=long_ema, adjust=False).mean()
    data['short_gradient'] = 0
    data['med_gradient'] = 0
    data['long_gradient'] = 0
    data = data[data['long_EWM'] != None]
    for index, row in data.iterrows():
        loc = data.index.get_loc(index)
        previous_data = data.iloc[loc-1]
        if previous_data['short_EWM'] < row.short_EWM:
            data.loc[index,'short_gradient'] = 1
        elif previous_data['short_EWM'] > row.short_EWM:
            data.loc[index, 'short_gradient'] = -1
        if previous_data['med_EWM'] < row.med_EWM:
            data.loc[index,'med_gradient'] = 1
        elif previous_data['med_EWM'] > row.med_EWM:
            data.loc[index, 'med_gradient'] = -1
    # If the short EWM is positive and the 180 EWM is lower than the average means its a buy
    data['signal'] = 0
    data.loc[(data['short_gradient'] == 1) & (data['long_EWM'] < data['Close']), 'signal'] += 1
    data.loc[(data['short_gradient'] == -1) & (data['long_EWM'] > data['Close']), 'signal'] -= 1
    data.loc[(data['med_gradient'] == 1) & (data['long_EWM'] < data['Close']), 'signal'] += 0.5
    data.loc[(data['med_gradient'] == -1) & (data['long_EWM'] > data['Close']), 'signal'] -= 0.5
    return data

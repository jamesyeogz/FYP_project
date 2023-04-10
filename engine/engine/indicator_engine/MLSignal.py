
import tensorflow as tf
import pathlib
import sys
import datetime
import time
import yfinance as yf
import copy
from baseSignal import Signal
import pandas as pd
scriptpath = pathlib.Path(__file__).parent.resolve()
sys.path.append(str(scriptpath.parent.parent/'utils'))
from dict_utils import Df_to_Dict, get_future_days_stock
from postgres import db_conn, MachineLearningTables
from tables.StockPrice import MainMLPrice

class MLSignal(Signal):
    table_dict = {
        'MTPrice': {
            'Day1': 0,
            'Day2': 1
        },
        'TWPrice': {
            'Day1': 1,
            'Day2': 2
        },
        'WTPrice': {
            'Day1': 2,
            'Day2': 3
        },
        'TFPrice': {
            'Day1': 3,
            'Day2': 4
        },
    }
    table_names = ['MTPrice', 'TFPrice', 'TWPrice', 'WTPrice']
    
    def __init__(self, dataobj,mlclass=None) -> None:
        self.db_conn = db_conn()
        super().__init__(conn=self.db_conn, name='MLSignal',
                              function=self.defaultFunction, dataclass=dataobj,ml=mlclass)
        self.dataobj = dataobj
        if not mlclass:
            self.mlclass = MachineLearningTables(self.table_names)
            self.mlclass.createMachineLearningTable()
            self.tables = self.mlclass.tables
        if mlclass:
            self.mlclass = mlclass
            self.tables = self.mlclass.tables

    def defaultFunction(self):
        return

    def GetDfWithSignal(self,data=None):
        if not data:
            data = yf.download(tickers='SPY',start= "2023-01-01", end="2023-03-31")
            # data = self.get_price_from_yf(period='5d')
        data['Previous_Close'] = (data.Close.shift(1))
        data['signal'] = 0.0
        for d in self.table_dict:
            num_minus = 1
            if self.table_dict[d]['Day1'] == 0:
                num_minus = 3
            mldata =self.db_conn.SelectAll(self.tables[d])
            df = pd.DataFrame.from_dict(mldata)
            df.set_index('Date',inplace=True)
            data = pd.concat([data,df],axis='columns')
            for index,row in data.iterrows():
                if not pd.isna(row.Predicted_Close) and index.dayofweek == self.table_dict[d]['Day1']:
                    string_date = pd.to_datetime(index)-datetime.timedelta(days=num_minus)
                    query=string_date.strftime('%Y-%m-%d')
                    if row.Predicted_Close > row.Previous_Close:
                        data.loc[query,'signal'] += 1
                    else:
                        data.loc[query,'signal'] -= 1
                if not pd.isna(row.Predicted_Close) and index.dayofweek == self.table_dict[d]['Day2']:
                    string_date = pd.to_datetime(index)-datetime.timedelta(days=1)
                    query=string_date.strftime('%Y-%m-%d')
                    if row.Predicted_Close > row.Previous_Close:
                        data.loc[query,'signal'] += 0.5
                    else:
                        data.loc[query,'signal'] -= 0.5
            data.drop('Predicted_Close',inplace=True,axis='columns')
        return data
    def getTableData(self):
        return self.db_conn.SelectAll(self.dataobj)

    def RunDatesWithSignal(self,data=None):
        if not data:
            data = yf.download(tickers='SPY',start= "2023-01-01", end="2023-03-31")
        
        
        
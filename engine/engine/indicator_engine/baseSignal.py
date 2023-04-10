import pandas as pd
import numpy as np
import yfinance as yf
from Turtle_agent import GetSMA
import pathlib,sys
import time
import copy
scriptpath = pathlib.Path(__file__).parent.resolve()
sys.path.append(str(scriptpath.parent.parent/'utils'))
from postgres import db_conn,MachineLearningTables
from tables.StockPrice import SMAPrice, MainMLPredictedPrice
from dict_utils import Df_to_Dict,get_future_days_stock
class Signal:
    def __init__(self,conn,name,function,dataclass,event=None,period='1m',**kw) -> None:
        self.event = event if event else None
        self.name = name
        self.postgres = conn
        self.dataclass = dataclass
        self.function = function
        self.period = period
        self.session = self.postgres.getSession()
        if kw.get('ml', ''):
            self.ml = kw['ml']
            self.classes = self.ml.getClasses()
        else:
            self.ml = MachineLearningTables(['MTPrice','TFPrice','TWPrice','WTPrice'])
            self.ml.createMachineLearningTable()
            self.classes= self.ml.getClasses()
        self.days_to_table ={
            1: 'MTPrice',
            2: 'TWPrice',
            3: 'WTPrice',
            4: 'TFPrice'
        }
        # Start the database function
        return

    def update_df_to_Tables(self,df,keys=['Predicted_Close','Close']):
        first = df.iloc[-1]
        session = self.postgres.getSession()
        database_obj = self.classes[self.days_to_table[first.name.dayofweek]]
        for index,row in df.iterrows():
            variables = Df_to_Dict(row,index,'Date',keys)
            new_data = {}
            if variables.get('Close',''):
                new_data['Predicted_Close'] = variables['Close']
            else:
                new_data['Predicted_Close'] = variables['Predicted_Close']
            new_data['Date'] = variables['Date']
            query = session.query(database_obj).filter(database_obj.Date == new_data['Date'])
            results = self.postgres.Convertquery_toDict(query)
            if len(results) > 0:
                session.query(database_obj).filter_by(Date=new_data['Date']).update(new_data)
            else:
                dataclass = copy.deepcopy(database_obj)
                dataclass = dataclass(new_data)
                self.postgres.Insert(dataclass)
            # dataclass = copy.deepcopy(database_obj)
            # dataclass = dataclass(new_data)
            # self.postgres.Insert(dataclass)
        return
    def update_df_to_MLGraph(self,df):
        session = self.postgres.getSession()
        database_obj = MainMLPredictedPrice
        for index,row in df.iterrows():
            variables = Df_to_Dict(row,index,'Date',keys=['Predicted_Close'])
            new_data  = {}
            new_data['Close'] = variables['Predicted_Close']
            new_data['Date'] = variables['Date']
            query = session.query(database_obj).filter(database_obj.Date == new_data['Date'])
            results = self.postgres.Convertquery_toDict(query)
            if len(results) > 0:
                session.query(database_obj).filter_by(Date=new_data['Date']).update(new_data)
            else:
                dataclass = copy.deepcopy(database_obj)
                dataclass = dataclass(new_data)
                self.postgres.Insert(dataclass)
        return

    def update_df_to_database(self,df,keys,**kw):
        try:
            index_key = 'Date'
            if kw.get('index_key',''):
                index_key = kw['index_key']
            for index,row in df.iterrows():
                keys = keys
                variables = Df_to_Dict(row,index,index_key,keys)
                if self.CheckIfExist(index,variable='Date'):
                    self.UpdateExistingRow(variables)
                else:
                    dataclass = copy.deepcopy(self.dataclass)
                    dataclass = dataclass(variables)
                    self.postgres.Insert(dataclass)
            if self.event:
                self.event.set()
            return True
        except Exception as e:
            print(e)
            return False
    def UpdateExistingRow(self,data):
        session = self.postgres.getSession()
        old_data = session.query(self.dataclass).filter_by(Date=data['Date']).first()
        old_data = self.postgres.ConvertOneQuery(old_data)
        session.query(self.dataclass).filter_by(Date=data['Date']).update({
            'signal': old_data['signal'] + data['signal'],
            'Close' : data['Close'],
            'Open' : data['Open'],
            'Volume' : data['Volume']
        })
        return
    
    def CheckIfExist(self,date,variable):
        session = self.postgres.getSession()
        query = session.query(self.dataclass).filter(self.dataclass.Date == date)
        results = self.postgres.Convertquery_toDict(query)
        if len(results) > 0 and results[0].get(variable,''):
            return True
        else:
            return False
    def get_price(self,data=None):
        if not data:
            data= yf.download(tickers='SPY', period='1d', interval='1d')
        if not self.CheckIfExist(data.index[0],variable='Close'):
            data = self.get_price_from_yf(period=self.period)
            data = self.function(data)
            if len(data.index)>0:
                self.update_df_to_Tables(data[3:])
                self.update_df_to_MLGraph(data[5:])
                self.update_df_to_database(data[:-1],keys=self.dataclass.keys)
        return
    def get_price_specific(self,data,start,end):
        if not self.CheckIfExist(data.index[-1],variable='Close'):
            data = yf.download(tickers='SPY',start=start,end=end,interval='1d')
            data = self.function(data)
            if len(data.index)>0:
                # data.iloc[3:]
                self.update_df_to_Tables(data[4:])
                self.update_df_to_MLGraph(data[5:])
                self.update_df_to_database(data[:-1],keys=self.dataclass.keys)
        return
    def get_price_from_yf(self,period='1mo'):
        return yf.download(tickers='SPY',period=period,interval='1d')
import collections
from Turtle_agent import GetSMA
import threading
import sys,pathlib
import yfinance as yf
import time
import datetime
from baseSignal import Signal
from MLModel import GetResults2Days
scriptpath = pathlib.Path(__file__).parent.resolve()
sys.path.append(str(scriptpath.parent.parent/'utils'))
from postgres import db_conn
from dict_utils import Df_to_Dict,get_future_days_stock
from tables.StockPrice import SMAPrice,MainMLPrice

from tables.Users import Users
from tables.Accounts import Accounts
from tables.History import History
# Manages all the Signals

class SignalManager:
    given_signals =[
        # {'name':'SMASignal','function':GetSMA,'dataclass':SMAPrice,'period':'1m'},
        {'name':'ML_indicator','function':GetResults2Days,'dataclass':MainMLPrice,'period': '5d'}
        ]
    def __init__(self,start=True) -> None:
        self.postgres = db_conn()
        self.processes = {}
        self.events = {}
        self.signals = {}
        if start:
            for signal in self.given_signals:
                self.events[signal['name']] = threading.Event()
                self.signals[signal['name']] = Signal(self.postgres,name=signal['name'],function=signal['function'],dataclass=signal['dataclass'],event=self.events[signal['name']],period=signal['period'])
            for key,signal in self.signals.items():
                start_timer = Run_Process_Function(signal.get_price)
                self.start_process(start_timer.run,key)
            for signal in self.given_signals:
                simulator = RealTimeSimulator(event=self.events[signal['name']],db_conn=self.postgres,database_obj=signal['dataclass'],signal=signal['name'])
                self.start_process(simulator.start_run,f'{signal["name"]}_Simulator')
            self.run_manager()
    def run_manager(self):
        while True:
            time.sleep(100)
            print(f"Manager is running.... on {datetime.datetime.now()}")
    def start_process(self,function,name):
        process =threading.Thread(target=function,daemon=True)
        self.processes[name] = process
        self.processes[name].start()
        return
    def start_run(self):
        # self.tradeMachine =TradeMachine(amount=6000,shares=4,no_shares=2)
        return
    def start_backtest(self,data,signal="SMA_indicator",**kw):
        # For BackTesting we need:
        '''
        1. Data from the signals that was collected and stored 
        2. Name of the stock Price
        3. Original amount
        4. The maximum number of shares that you can buy
        '''
        self.backtest = Backtest(data=data,db_conn=self.postgres,signal=signal,**kw)
        self.backtest.start_backtest()
        return
    def GetDataFromDB(self,classobj):
        return self.postgres.SelectAll(classobj)

# This class will run a function individually based on the either the time or the trigger of the event

class Run_Process_Function:
    def __init__(self,function,event=None):
        self.event= None
        self.function = function
        if not event:
            future,t = get_future_days_stock()
            self.next_time = (future-t).total_seconds()
        if event:
            self.event = event
        return
    def run(self):
        self.function()
        while True:
            if self.event:
                self.event.wait()
                self.function()
                self.event.clear()
            else:
                time.sleep(self.next_time)
                self.function()
                future,t = get_future_days_stock()
                self.next_time = (future-t).total_seconds()

class TradeMachine:
    def __init__(self,db_conn,signal='SMA_indicator',no_shares=1,indicator=1):
        # The no_shares is the amount to buy at one time,
        # The total_shares is the total number of shares you can keep
        # The shares are the number of shares the app currently holds
        self.shares = 0
        self.no_shares = no_shares
        self.signal = signal
        # The indicator is the strength of the signal where you wan to buy
        self.minimum_indicator = indicator
        if db_conn:
            self.db_conn = db_conn
        self.queue = collections.deque()
        # CoolDown period whenever a trade is executed
        self.time_to_restrict = 3
        self.restrict = 0
        return
    def Run_Test_Data(self,data,index=None):
        if self.queue:
            indicator = self.queue.popleft()
            if indicator == 'Buy':
                self.TestBuy(data,index)
            elif indicator == 'Sell':
                self.TestSell(data,index)
        if self.restrict:
            self.restrict -= 1
            return
        if data['signal'] >= self.minimum_indicator:
            self.queue.append('Buy')
            self.restrict =  self.time_to_restrict
        elif data['signal'] <= -self.minimum_indicator:
            self.queue.append('Sell')
            self.restrict = self.time_to_restrict
        return
    def TestBuy(self, data,index=None):
        session = self.db_conn.getSession()
        # results = session.query(Accounts).filter()/
        results = session.query(Accounts).filter(Accounts.indicator == self.signal)
        results = self.db_conn.Convertquery_toDict(results)
        for result in results:
            if result['holding'] < result['maxshares']:
                total = data['Open']*self.no_shares
                result['holding'] += self.no_shares
                result['value'] -= total
                self.UpdateAccount(result)
                history = result
                history['buy'] = data['Open']
                if index:
                    history['Date'] = index
                self.CreateHistory(result)
        return
    
    def TestSell(self, data,index=None):
        session = self.db_conn.getSession()
        results = session.query(Accounts).filter(Accounts.indicator == self.signal)
        results = self.db_conn.Convertquery_toDict(results)
        for result in results:
            if result['holding']-self.no_shares >= 0:
                total = data['Open']*self.no_shares
                result['holding'] -= self.no_shares
                result['value'] += total
                self.UpdateAccount(result)
                history = session.query(History).filter(History.account_id==result['id'],History.sell == None).first()
                history = self.db_conn.ConvertOneQuery(history)
                history['sell'] = data['Open']
                history['profit'] = float(history['sell']) - float(history['buy'])
                if index:
                    history['Date'] = index
                self.UpdateHistory(history)
        return
    
    def End(self,data):
        session = self.db_conn.getSession()
        results = session.query(Accounts).filter(Accounts.indicator == self.signal)
        results = self.db_conn.Convertquery_toDict(results)
        for result in results:
            if result['holding'] > 0:
                for i in range(result['holding']):
                    self.TestSell(data)
        return
    def Calculate(self,amount=None,original=3000):
        percentage = ((amount-original)/original*100)
        profit =amount-original
        return profit, round(percentage,2)
    def UpdateAccount(self,data):
        session = self.db_conn.getSession()
        session.query(Accounts).filter(Accounts.id == data['id']).update(data)
        session.commit()
        return
    def CreateHistory(self,data):
        session = self.db_conn.getSession()
        data['account_id'] = data['id']
        insert = History(data)
        session.add(insert)
        session.commit()
        return
    def UpdateHistory(self,data):
        session = self.db_conn.getSession()
        if not data.get('Date',''):
            data['Date'] = datetime.datetime.today()
        session.query(History).filter(History.id == data['id']).update(data)
        session.commit()
        return


class Backtest(TradeMachine):
    def __init__(self,data,db_conn,signal='SMA_indicator',**kw) -> None:
        super().__init__(db_conn=db_conn,signal=signal,**kw)
        self.test_data = data
        return
    def start_backtest(self):
        for i, (index, row) in enumerate(self.test_data.iterrows()):
            if i == len(self.test_data) - 1:
                self.End(row)
            else:
                self.Run_Test_Data(row,index=index)
        session = self.db_conn.getSession()
        results = session.query(Accounts).filter(Accounts.indicator == self.signal)
        results = self.db_conn.Convertquery_toDict(results)
        for result in results:
            print(self.Calculate(amount=result['value']))
        return


class RealTimeSimulator(TradeMachine):
    def __init__(self,event,db_conn,database_obj,signal='SMA_indicator') -> None:
        super().__init__(db_conn=db_conn,signal=signal)
        self.date = datetime.datetime.today()
        self.event = event
        self.db_conn = db_conn
        self.database_obj = database_obj
        self.queue = collections.deque()
    
    def start_run(self):
        while True:
            self.event.wait()
            data = self.db_conn.getLastQueryForDate(self.database_obj)
            self.Run_Test_Data(data)
            self.event.clear()

s = SignalManager()
# data = s.GetDataFromDB(MainMLPrice)
# import pandas as pd
# data = pd.DataFrame.from_dict(data)
# data.set_index('Date',inplace=True)
# s.start_backtest(data=data,signal='MLSignal',indicator=1.5)
# sign = SignalManager()
# data = yf.download(tickers='SPY',period='1y',interval='1d')
# data = GetSMA(data=data)
# sign.start_backtest(data=data)

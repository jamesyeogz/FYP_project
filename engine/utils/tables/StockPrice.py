from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey,REAL,Column,String, Integer,ARRAY,Date,Numeric,BigInteger
from .d_base import Base
# class Price(Base):
#     __tablename__ = "MLSignal"
#     Date = Column('Date',Date,primary_key=True)
#     Close = Column('Close',Numeric(6,2))
#     Signal = Column('signal', REAL)
#     Open = Column('Open',Numeric(6,2))
#     Volume = Column('Volume',BigInteger)

#     def __init__(self,variables) -> None:
#         self.Open  = variables['Open']
#         self.Volume = variables['Volume']
#         self.Date = variables['Date']
#         self.Close = variables['Close']
#         self.Signal = variables['signal']

        

# class StockPrice(Base):
#     __tablename__ = ""
#     user = Column('user',String,primary_key=True)
#     password = Column('password', String)
#     models = Column('models', ARRAY(String))

#     def __init__(self,user,password,models) -> None:
#         self.user = user
#         self.password = password
#         self.models = models
class MainMLPredictedPrice(Base):
    __tablename__ = "ML_MainPredictedGraph"
    Date = Column('Date',Date,primary_key=True)
    Close = Column('Close', Numeric(6,2))
    keys=['Predicted_Close','Date']
    def __init__(self,variables):
        self.Date = variables['Date']
        self.Close = variables['Close']



class MainMLPrice(Base):
    __tablename__ = "ML_indicator"
    Date = Column('Date',Date,primary_key=True)
    Open =  Column('Open',Numeric(6,2))
    Close = Column('Close',Numeric(6,2))
    Volume = Column('Volume',BigInteger)
    signal = Column('signal',REAL)
    keys=['Open','Close','Volume','signal']

    def __init__(self,variables):
        self.Open =  variables.get('Open','')
        self.Date = variables['Date']
        self.Close = variables.get('Close','')
        self.Volume = variables.get('Volume','')
        self.signal = variables['signal']
    

class SMAPrice(Base):
    __tablename__ = "SMA_indicator"
    Date = Column('Date',Date,primary_key=True)
    Open =  Column('Open',Numeric(6,2))
    Close = Column('Close',Numeric(6,2))
    Volume = Column('Volume',BigInteger)
    signal = Column('signal',REAL)
    RollingMax = Column('RollingMin',Numeric(6,2))
    RollingMin = Column('RollingMax',Numeric(6,2))
    keys=['Open','Close','Volume','signal','RollingMax','RollingMin']

    def __init__(self,variables):
        self.Open =  variables['Open']
        self.Date = variables['Date']
        self.Close = round(variables['Close'],2)
        self.Volume = variables['Volume']
        self.signal = variables['signal']
        self.RollingMax =round(variables['RollingMax'],2)
        self.RollingMin =round(variables['RollingMin'],2)
    
import sys, pathlib
scriptpath = pathlib.Path(__file__).parent.resolve()
sys.path.append(scriptpath.parent)
from extensions import db
from sqlalchemy import ForeignKey,Column,String, Integer,ARRAY,Date,Numeric
class MTPrice(db.Model):
    __tablename__ = "MTPrice"
    Date = Column('Date', Date,primary_key=True)
    Close = Column('Predicted_Close',Numeric(6,2))

    def __init__(self,variables) -> None:
        self.Date = variables['Date']
        self.Close = variables['Predicted_Close']
        return
class TWPrice(db.Model):
    __tablename__ = "TWPrice"
    Date = Column('Date', Date,primary_key=True)
    Close = Column('Predicted_Close',Numeric(6,2))

    def __init__(self,variables) -> None:
        self.Date = variables['Date']
        self.Close = variables['Predicted_Close']
        return
class WTPrice(db.Model):
    __tablename__ = "WTPrice"
    Date = Column('Date', Date,primary_key=True)
    Close = Column('Predicted_Close',Numeric(6,2))

    def __init__(self,variables) -> None:
        self.Date = variables['Date']
        self.Close = variables['Predicted_Close']
        return
class TFPrice(db.Model):
    __tablename__ = "TFPrice"
    Date = Column('Date', Date,primary_key=True)
    Close = Column('Predicted_Close',Numeric(6,2))

    def __init__(self,variables) -> None:
        self.Date = variables['Date']
        self.Close = variables['Predicted_Close']
        return
class MainMLPredictedPrice(db.Model):
    __tablename__ = "ML_MainPredictedGraph"
    Date = Column('Date',Date,primary_key=True)
    Close = Column('Close', Numeric(6,2))
    def __init__(self,variables):
        self.Date = variables['Date']
        self.Close = variables['Close']

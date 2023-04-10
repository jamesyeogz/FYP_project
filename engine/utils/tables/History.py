from sqlalchemy.orm import declarative_base
import datetime
from sqlalchemy import ForeignKey,Column,String, Integer,ARRAY,Numeric,Date
from .d_base import Base
class History(Base):
    __tablename__ = "history"
    id = Column('id',Integer,primary_key=True)
    user = Column('user',String)
    account_id = Column('account_id',Integer)
    buy= Column('buy',Numeric(6,2))
    sell = Column('sell',Numeric(6,2))
    profit= Column('profit',Numeric(6,2))
    Date = Column('Date',Date)

    def __init__(self,variables) -> None:
        self.user = variables['user']
        self.account_id = variables['account_id']
        self.buy = variables['buy']
        self.sell = variables['sell'] if variables.get('sell') else None
        self.profit = variables['profit'] if variables.get('profit') else None
        self.Date = variables['Date'] if variables.get('Date') else datetime.datetime.today()
        return


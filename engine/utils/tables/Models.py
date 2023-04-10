from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Numeric,ForeignKey,Column,String, Integer,ARRAY,BigInteger,Identity
from .d_base import Base
class Models(Base):
    __tablename__ = "models"
    id = Column('id', Integer, Identity(start=1, cycle=True), primary_key=True)
    indicator = Column('indicator', String)
    percentage = Column('percentage',Numeric(4,2))
    description = Column('description',String)

    def __init__(self,id,indicator,percentage,description) -> None:
        self.id = id
        self.indicator = indicator
        self.percentage = percentage
        self.description = description
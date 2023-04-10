import sys,pathlib
scriptpath = pathlib.Path(__file__).parent.resolve()
sys.path.append(scriptpath.parent)
from extensions import db
from sqlalchemy import ForeignKey,Numeric,Column,String, Integer,ARRAY,BigInteger

class Models(db.Model):
    __tablename__ = "models"
    id = Column('id', String,primary_key=True)
    indicator = Column('indicator', String)
    percentage = Column('percentage',Numeric(4,2))
    description = Column('description',String)

    def __init__(self,indicator,percentage,description) -> None:
        self.indicator = indicator
        self.percentage = percentage
        self.description = description
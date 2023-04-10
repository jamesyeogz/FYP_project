import sys, pathlib
scriptpath = pathlib.Path(__file__).parent.resolve()
sys.path.append(scriptpath.parent)
from extensions import db
from sqlalchemy import ForeignKey,Column,String, Integer,ARRAY,DOUBLE_PRECISION,Numeric
class Accounts(db.Model):
    __tablename__ = "accounts"
    id = Column('id',Integer,primary_key=True)
    user = Column('user',String)
    value = Column('value',Numeric(10,2))
    indicator = Column('indicator',String)
    maxshares = Column('maxshares',Integer)
    holding = Column('holding',Integer,default=0)

    def __init__(self,variables) -> None:
        if variables.get('id',''):
            self.id = variables['id']
        self.user = variables['user']
        self.value = variables['value']
        self.indicator = variables['indicator']
        self.maxshares = variables['maxshares']
        return

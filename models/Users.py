import sys,pathlib
scriptpath = pathlib.Path(__file__).parent.resolve()
sys.path.append(scriptpath.parent)
from extensions import db
from sqlalchemy import ForeignKey,Column,String, Integer,ARRAY

class User(db.Model):
    __tablename__ = "users"
    user = Column('user',String,primary_key=True)
    password = Column('password', String, nullable=False)

    def __init__(self,variables):
        self.user = variables['user']
        self.password = variables['password']


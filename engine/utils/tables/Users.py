from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey,Column,String, Integer,ARRAY
from .d_base import Base

class Users(Base):
    __tablename__ = "users"
    user = Column('user',String,primary_key=True)
    password = Column('password', String)

    def __init__(self,user,password) -> None:
        self.user = user
        self.password = password

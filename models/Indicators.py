from ..extensions import db

from sqlalchemy import create_engine
from sqlalchemy import ForeignKey,Column,String, Integer,ARRAY
class Indicators(db.Model):
    __tablename__ = "indicators"
    name = Column('name',String,primary_key=True)
    table_name = Column('table_name',String)

    def __init__(self,name,table_name) -> None:
        self.name = name
        self.table_name = table_name

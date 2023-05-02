import psycopg2
import os
from sqlalchemy import create_engine,MetaData,inspect
from sqlalchemy import ForeignKey,Column,String, Integer,ARRAY,Table,Date,Numeric
from sqlalchemy.orm import sessionmaker,declarative_base
from tables import Base
import os
class db_conn:
    def __init__(self,heroku=False) -> None:
        self.Base = Base
        # Initiates all the models
        if not heroku:
            self.conn = create_engine('postgresql://postgres:password@localhost:5432/flask_db')
            # self.conn = create_engine(os.environ['DATABASE_URL_NOW'])
        else:
            DATABASE_URL = os.environ.get("DATABASE_URL_NOW")
            self.conn = create_engine(DATABASE_URL)
        session = sessionmaker(bind=self.conn)
        self.session = session()
        return
    def Insert(self,classobj):
        # user = classobj("James","password",['model1','model2'])
        self.session.add(classobj)
        self.session.commit()
        return
    def Convertquery_toDict(self,rows):
        dict_arr = []
        for row in rows:
            dictret = dict(row.__dict__); dictret.pop('_sa_instance_state', None)
            dict_arr.append(dictret)
        return dict_arr
    def ConvertOneQuery(self,data):
        dictret = dict(data.__dict__)
        dictret.pop('_sa_instance_state', None)
        return dictret
    def SelectAll(self,classobj):
        results = self.session.query(classobj).all()
        return self.Convertquery_toDict(results)
    def Select(self,classobj,value):
        results = self.session.query(classobj).filter(classobj.Date == value)
        return self.Convertquery_toDict(results)
    
    def getEngine(self):
        return self.conn.connect()
    def getSession(self):
        return self.session
    def createTable(self,table):
        table.__table__.create(self.conn)
        return
    def deleteAll(self,classobj):
        return
    def getLastQueryForDate(self,classobj):
        result = self.session.query(classobj).order_by(classobj.Date.desc()).first()
        return self.ConvertOneQuery(result)
    def createAllTables(self):
        self.Base.metadata.create_all(bind=self.conn)
        return




class MachineLearningTables(db_conn):
    def __init__(self,table_names) -> None:
        super().__init__()
        self.tables = {} 
        self.table_names = table_names
    def createMachineLearningTable(self):
        for table_name in self.table_names:
            if not inspect(self.conn).has_table(table_name):
                table =  Table(
                    table_name,
                    MetaData(),
                    Column('Date',Date,primary_key=True),
                    Column('Predicted_Close',Numeric(6,2)))
                table.create(self.conn)
            self.tables[table_name]= self.createClass(table_name)
    def createClass(self,table_name):
        class CustomMLPrice(Base):
            __table_args__ = {'extend_existing': True} 
            __tablename__ = table_name
            Date = Column('Date',Date,primary_key=True)
            Predicted_Close = Column('Predicted_Close',Numeric(6,2))
            def __init__(self,variables):
                self.Date = variables['Date']
                self.Predicted_Close = variables['Predicted_Close']
        return CustomMLPrice

    def getClasses(self):
        return self.tables
    
    def DropTables(self,tables=[]):
        for table in tables:
            metadata = MetaData()
            metadata.reflect(bind=self.conn)
            table = metadata.tables.get(table)
            if table is not None:
                self.Base.metadata.drop_all(self.conn, [table],checkfirst=True)
        return 

        



        
        
        




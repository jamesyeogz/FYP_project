from postgres import db_conn
from sqlalchemy import Table,ForeignKey,Column,String, Integer,ARRAY,Date,Numeric,BigInteger
from sqlalchemy.orm import sessionmaker,declarative_base
from postgres import MachineLearningTables
from tables import Models,MainMLPrice,MainMLPredictedPrice,Users,Accounts
import tables
from werkzeug.security import generate_password_hash
import yfinance as yf 
# Uploading the tables into the place
import pathlib,sys,os
from dict_utils import Df_to_Dict
import pandas as pd
import datetime

table = tables
scriptpath = pathlib.Path(__file__).parent.resolve()
folderpath = scriptpath.parent/'data'
sys.path.append(str(folderpath))
db = db_conn()
session = db.getSession()
files = []
for file in os.listdir(folderpath):
    # print(os.path.join(file,folderpath))
    if os.path.isfile(os.path.join(folderpath,file)):
        files.append(str(os.path.join(folderpath,file)))

# Get the Machineleaning classes
ml = MachineLearningTables(['MTPrice','TFPrice','TWPrice','WTPrice'])
ml.createMachineLearningTable()
classes = ml.getClasses()
db.createAllTables()

scriptpath = pathlib.Path(__file__).parent.resolve()
folderpath = scriptpath.parent/'engine'/'indicator_engine'
sys.path.append(str(folderpath))
from engine import SignalManager
from baseSignal import Signal
from MLModel import GetResults2Days

signal = Signal(db,name='ML_indicator',function=GetResults2Days,dataclass=MainMLPrice,event=None,period='5d')
data = yf.download(tickers='SPY',start='2023-01-01',end='2023-04-10')
for i in range(len(data)-5):
    parse_data = data.iloc[i:i+5]
    signal.get_price_specific(data=data,start=parse_data.index[0],end=parse_data.index[-1])


# Creating Users
user = Users(user='James',password=generate_password_hash('password'))
db.Insert(user)

# Creating Accounts
account = Accounts(variables={'user':'James','value':3000,'indicator':'ML_indicator','maxshares': 3})
db.Insert(account)

# Add Model
model = Models(id=1,indicator='ML_indicator', percentage=60.45, description='This is the Model')
db.Insert(model)

# Backtesting Account
s = SignalManager(start=False)
data = s.GetDataFromDB(MainMLPrice)
data = pd.DataFrame.from_dict(data)

data = data.mask(data.eq('None')).dropna()
data.set_index('Date',inplace=True)
print(data)
s.start_backtest(data=data,signal='ML_indicator',indicator=1.5)
# filtered.sort(key=lambda item:item['Date'])



# s = SignalManager()
# Run This year's data all together











# def update_df_to_MLGraph(df):
#     session = db.getSession()
#     database_obj = MainMLPredictedPrice
#     for index,row in df.iterrows():
#         that_date  = pd.to_datetime(row.Date)
#         variables = Df_to_Dict(row,index,'Date',keys=MainMLPredictedPrice.keys)
#         data = session.query(MainMLPredictedPrice).filter_by(Date=str(that_date)).first()
#         if not data:
#             new_data  = {}
#             new_data['Close'] = variables['Predicted_Close']
#             new_data['Date'] = variables['Date']
#             dataclass = database_obj(new_data)
#             db.Insert(dataclass)
#         if data:
#             session.query(MainMLPredictedPrice).filter(MainMLPredictedPrice.Date==str(that_date)).update({'Close':variables['Predicted_Close']})
#     return
# scriptpath = pathlib.Path(__file__).parent.resolve()
# folderpath = scriptpath.parent/'engine'/'indicator_engine'
# sys.path.append(str(folderpath))
# from MLSignal import MLSignal

# ms = MLSignal(dataobj=MainMLPrice,mlclass=ml)
# data = ms.GetDfWithSignal()
# ms.update_df_to_database(data,keys=MainMLPrice.keys)

# # ml.DropTables(['MTPrice','TFPrice','TWPrice','WTPrice'])
# first_days = [0,3,1,2]
# number= -1
# for file in files:
#     number += 1
#     first = first_days[number]
#     name = os.path.basename(file).split('.')[0]
#     df = pd.read_csv(file)
#     update_df_to_MLGraph(df)
#     for index, row in df.iterrows():
#         that_date  = pd.to_datetime(row.Date)
#         if that_date.dayofweek == first:
#             date_range_add = that_date - datetime.timedelta(days=1 if first!=0 else 3)
#             prev_data = session.query(MainMLPrice).filter_by(Date=str(date_range_add)).first()
#             prev_data = db.ConvertOneQuery(prev_data)
#             new_data = {}
#             new_data['Predicted_Close'] = prev_data['Close']
#             new_data['Date'] = prev_data['Date']
#             insert = classes[name](variables=new_data)
#             db.Insert(insert)
#         data = Df_to_Dict(row,None,None,['Date','Predicted_Close'])
#         insert = classes[name](variables=data)
#         db.Insert(insert)     

#         # else:
            

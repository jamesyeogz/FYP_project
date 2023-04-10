import sys, pathlib
scriptpath = pathlib.Path(__file__).parent.resolve()
sys.path.append(scriptpath.parent)
from serialization import ML_indicator_Schema,Accounts_Serializer,Model_Serializer,History_Serializer,SMA_indicator_Schema,MTPrice_Serializer,TWPrice_Serializer,WTPrice_Serializer,TFPrice_Serializer,MainMLModel_Serializer
from extensions import db
from models import Models,ML_indicator,SMA_indicator,Accounts,History,MTPrice,TWPrice,WTPrice,TFPrice,MainMLPredictedPrice
from flask import Blueprint,jsonify,request,abort
from flask_jwt_extended import get_jwt_identity,get_current_user,jwt_required
import datetime
from sqlalchemy import func


indicators ={
    'ML_indicator' : {
    'table': ML_indicator,
    'schema': ML_indicator_Schema
    },
    'SMA_indicator' : {
    'table': SMA_indicator,
    'schema': SMA_indicator_Schema
    },
}
def GetTradeCount(user_accounts):
    number = 0
    for user in user_accounts:
        total_count = History.query.filter_by(account_id=user['id'])
        history_filter = History_Serializer(many=True)
        number += len(history_filter.dump(total_count))
    return number
def getModelQuery(id):
    result = Models.query.filter_by(id=id).first()
    model = Model_Serializer()
    return model.dump(result)

def getModelStatsGeneral(id):
    result,schema,name = getModelById(id)
    total =Accounts.query.filter_by(indicator=name).with_entities(func.sum(Accounts.value).label('total')).first().total
    user_accounts = Accounts.query.filter_by(indicator=name)
    account_filter = Accounts_Serializer(many=True)
    user_accounts = account_filter.dump(user_accounts)
    value = 0
    for account in user_accounts:
        history = History.query.filter_by(account_id=account['id']).with_entities(func.sum(History.profit).label('profit')).first().profit
        if history:
            value += history
    return name,total,value

def getModelById(id):
    result = Models.query.filter_by(id=id).first()
    indicator = indicators[result.indicator]['table']
    schema = indicators[result.indicator]['schema']
    return indicator,schema,result.indicator



Dashboard = Blueprint('Dashboard',__name__)


@Dashboard.route('/user/stats',methods=['GET'])
@jwt_required()
def getUserStats():
    user = get_jwt_identity()
    total =Accounts.query.filter_by(user=user).with_entities(func.sum(Accounts.value).label('total')).first().total
    user_accounts = Accounts.query.filter_by(user=user)
    account_filter = Accounts_Serializer(many=True)
    user_accounts = account_filter.dump(user_accounts)
    value = 0
    total_count = GetTradeCount(user_accounts)
    for account in user_accounts:
        history = History.query.filter_by(account_id=account['id']).with_entities(func.sum(History.profit).label('profit')).first().profit
        if history:
            value += history
    return jsonify(total=total,profit=value,total_count=total_count),200

@Dashboard.route('/mainml/<period>',methods=['GET'])
@jwt_required()
def getMainMLModel(period):
    today = datetime.datetime.today()
    last_date = today-datetime.timedelta(days=int(period))
    results = MainMLPredictedPrice.query.filter(MainMLPredictedPrice.Date >= last_date)
    filter_schema = MainMLModel_Serializer(many=True)
    filtered = filter_schema.dump(results)
    filtered.sort(key=lambda item:item['Date'])
    return jsonify(filtered),200


@Dashboard.route('/ml/<period>', methods=['GET'])
# @jwt_required()
def getMLModels(period):
    models = [[MTPrice,MTPrice_Serializer],[TWPrice,TWPrice_Serializer],[WTPrice,WTPrice_Serializer],[TFPrice,TFPrice_Serializer]]
    data = []
    today = datetime.datetime.today()
    last_date = today-datetime.timedelta(days=int(period))
    for model in models:
        results = model[0].query.filter(model[0].Date >= last_date)
        filter_schema = model[1](many=True)
        filtered = filter_schema.dump(results)
        num = 0
        while num < int(period):
            test = last_date+datetime.timedelta(days=num)
            if not any(d['Date'] == test.strftime("%Y-%m-%d") for d in filtered):
                filtered.append({'Date':test.strftime("%Y-%m-%d"),'Close':None})
            num +=1
        filtered.sort(key=lambda item:item['Date'])
        data.append(filtered)
    return jsonify(data),200

@Dashboard.route('/<id>/<period>',methods=['GET'])
@jwt_required()
def getModel(id,period):
    result = Models.query.filter_by(id=id).first()
    indicator = indicators[result.indicator]['table']
    today = datetime.datetime.today()
    last_date = today-datetime.timedelta(days=int(period))
    results = indicator.query.filter(indicator.Date >= last_date)
    filter_schema = indicators[result.indicator]['schema'](many=True)
    data = filter_schema.dump(results)
    data.sort(key=lambda item:item['Date'])
    return jsonify(data),200

@Dashboard.route('/<id>/general')
@jwt_required()
def getGeneral(id):
    results = Models.query.filter_by(id=id).first()
    model_filter = Model_Serializer()
    result = model_filter.dump(results)
    return result,200


@Dashboard.route('/<id>/stats', methods=['GET'])
@jwt_required()
def getModelStats(id):
    result,schema,name = getModelById(id)
    total =Accounts.query.filter_by(indicator=name).with_entities(func.sum(Accounts.value).label('total')).first().total
    user_accounts = Accounts.query.filter_by(indicator=name)
    account_filter = Accounts_Serializer(many=True)
    user_accounts = account_filter.dump(user_accounts)
    value = 0
    total_count = GetTradeCount(user_accounts)
    for account in user_accounts:
        history = History.query.filter_by(account_id=account['id']).with_entities(func.sum(History.profit).label('profit')).first().profit
        if history:
            value += history
    return jsonify(name=name,total=total,profit=value,total_count=total_count),200

@Dashboard.route('/history')
@jwt_required()
def getHistory():
    user = get_jwt_identity()
    accounts = Accounts.query.filter_by(user=user)
    account_serializer = Accounts_Serializer(many=True)
    accounts = account_serializer.dump(accounts)
    account_ids = []
    for account in accounts:
        account_ids.append(account['id'])
    histories = History.query.filter(History.account_id.in_(account_ids))
    history_serializer = History_Serializer(many=True)
    history = history_serializer.dump(histories)
    return history,200


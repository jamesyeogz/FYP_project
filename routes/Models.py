import sys, pathlib
scriptpath = pathlib.Path(__file__).parent.resolve()
sys.path.append(scriptpath.parent)
from serialization import ML_indicator_Schema,Accounts_Serializer,Model_Serializer,History_Serializer
from extensions import db
from models import Models,ML_indicator,SMA_indicator,Accounts,History
from flask import Blueprint,jsonify,request,abort
from flask_jwt_extended import get_jwt_identity,get_current_user,jwt_required
import datetime
from sqlalchemy import func
indicators ={
    'ML_indicator' : {
    'table': ML_indicator,
    'schema': ML_indicator_Schema
    },
    'SMA_indicator': SMA_indicator
}

Model = Blueprint('models',__name__)

@Model.route('/GetAccounts', methods=['GET'])
@jwt_required()
def GetAccounts():
    user = get_jwt_identity()
    result = Accounts.query.filter_by(user=user)
    filter_schema = Accounts_Serializer(many=True)
    data=  filter_schema.dump(result)
    return jsonify(data),200

@Model.route('/AddAccount',methods=['POST'])
@jwt_required()
def AddAccount():
    user= get_jwt_identity()
    value = int(request.json.get('value',''))
    max_shares = value//450
    variables ={
        'user' : user,
        'indicator' : request.json.get('indicator',''),
        'value' : value,
        'maxshares' : max_shares,
    }
    try:
        account = Accounts(variables=variables)
        db.session.add(account)
        db.session.commit()
        return jsonify(Action='Success'),200
    except Exception as e:
        return abort(400,{'Error':e})

@Model.route('/DeleteAccount',methods=['POST'])
@jwt_required()
def DeleteAccount():
    user = get_jwt_identity()
    delete = request.json.get('id','')
    if not delete:
        return abort(400)
    try:
        account = Accounts.query.filter_by(id=delete).first()
        filter  =Accounts_Serializer()
        data = filter.dump(account)
        if not data:
            return abort(400)
        if data['user'] != user:
            return abort(400)
        db.session.delete(account)
        db.session.commit()
        return jsonify(Action="Success"),200
    except Exception as e:
        return jsonify(Error=str(e)),400

@Model.route('/EditAccount/<id>', methods=['POST'])
@jwt_required()
def EditAccount(id):
    account = Accounts.query.filter_by(id=id).first()
    indicator = request.json['indicator']
    value= int(request.json['value'])
    account.value = request.json.get('value','')
    account.indicator = indicator
    account.maxshares = value//450
    db.session.commit()
    return jsonify(Action="Success"),200


        

    


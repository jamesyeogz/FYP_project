from werkzeug.security import generate_password_hash, check_password_hash
import sys, pathlib
scriptpath = pathlib.Path(__file__).parent.resolve()
sys.path.append(scriptpath.parent)
from extensions import db
from models import User
from flask import Blueprint,request,abort,jsonify
from flask_jwt_extended import create_access_token


auth = Blueprint('auth',__name__)
@auth.route('/register',methods=['POST'])
def register():
    print(request.json)
    variables ={
        'user': request.json.get('user',''),
        'password' : generate_password_hash(request.json.get('password',''))
    }
    if not variables['user'] or not variables['password']:
        return abort(400)
    user =User.query.filter_by(user=variables['user']).one_or_none()
    if user is not None:
        return abort(400,{'Error':'User already exist'})
    user = User(variables=variables)
    db.session.add(user)
    db.session.commit()
    return jsonify(Action='Success'),200

@auth.route('/login',methods=['POST'])
def login():
    user = request.json.get('user','')
    password = request.json.get('password','')
    if not user or not password:
        return abort(400)
    user = User.query.filter_by(user=user).first()
    if not user or not check_password_hash(user.password,password):
        return abort(401,  {"message": 'User or Password is wrong'})
    else:
        access_token = create_access_token(identity=user.user,additional_claims={'is_admin':True})
        response = jsonify(access_token=access_token,user=user.user)
        return response,200


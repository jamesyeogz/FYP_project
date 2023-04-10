from functools import wraps
from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from extensions import db,jwt
from routes import auth,Model,Dashboard
from flask_cors import CORS
app = Flask(__name__,static_folder='fe/build', static_url_path='/')
CORS(app)
app.config["JWT_SECRET_KEY"] = "super-secret"  #Required to Change this
# app.config ['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/flask_db'
app.config ['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db.init_app(app)
jwt.init_app(app)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(Model,url_prefix='/models')
app.register_blueprint(Dashboard,url_prefix='/dashboard')
@app.route('/')
def index():
    return app.send_static_file('index.html')

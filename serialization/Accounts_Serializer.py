from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import sys,pathlib
scriptpath = pathlib.Path(__file__).parent.resolve()
sys.path.append(scriptpath.parent)
from models import Accounts

class Accounts_Serializer(SQLAlchemyAutoSchema):
    class Meta:
        model = Accounts
        load_instance = True

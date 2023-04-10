from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import sys,pathlib
scriptpath = pathlib.Path(__file__).parent.resolve()
sys.path.append(scriptpath.parent)
from models import History

class History_Serializer(SQLAlchemyAutoSchema):
    class Meta:
        model = History
        load_instance = True

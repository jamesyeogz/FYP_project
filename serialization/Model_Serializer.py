from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import sys,pathlib
scriptpath = pathlib.Path(__file__).parent.resolve()
sys.path.append(scriptpath.parent)
from models import Models

class Model_Serializer(SQLAlchemyAutoSchema):
    class Meta:
        model = Models
        load_instance = True
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import sys,pathlib
scriptpath = pathlib.Path(__file__).parent.resolve()
sys.path.append(scriptpath.parent)
from models import ML_indicator

class ML_indicator_Schema(SQLAlchemyAutoSchema):
    class Meta:
        model = ML_indicator
        load_instance = True

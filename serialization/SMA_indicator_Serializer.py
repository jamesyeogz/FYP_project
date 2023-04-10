from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import sys,pathlib
scriptpath = pathlib.Path(__file__).parent.resolve()
sys.path.append(scriptpath.parent)
from models import SMA_indicator

class SMA_indicator_Schema(SQLAlchemyAutoSchema):
    class Meta:
        model = SMA_indicator
        load_instance = True

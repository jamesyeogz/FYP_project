from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import sys,pathlib
scriptpath = pathlib.Path(__file__).parent.resolve()
sys.path.append(scriptpath.parent)
from models import MTPrice,TWPrice,WTPrice,TFPrice,MainMLPredictedPrice

class MTPrice_Serializer(SQLAlchemyAutoSchema):
    class Meta:
        model = MTPrice
        load_instance = True

class TWPrice_Serializer(SQLAlchemyAutoSchema):
    class Meta:
        model = TWPrice
        load_instance = True

class WTPrice_Serializer(SQLAlchemyAutoSchema):
    class Meta:
        model = WTPrice
        load_instance = True

class TFPrice_Serializer(SQLAlchemyAutoSchema):
    class Meta:
        model = TFPrice
        load_instance = True

class MainMLModel_Serializer(SQLAlchemyAutoSchema):
    class Meta:
        model = MainMLPredictedPrice
        load_instance = True
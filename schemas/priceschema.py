from config import db,ma
from models.pricemodel import Prices
from marshmallow.fields import Nested
#from schemas.productschema import ProductGetSchema
from schemas.sizeschema import SizeGetSchema

class PriceSchema(ma.ModelSchema):

    class Meta:
        model = Prices
        fields = ("id","sizeId","productId","price")
        sqla_session = db.session

class PriceGetSchema(ma.ModelSchema):
    size_prices= ma.Nested(SizeGetSchema)
    class Meta:
        model = Prices
    #    fields = ("id","sizeId","productId","price")
        sqla_session = db.session

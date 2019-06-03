from models.sizemodel import Sizes
from config import ma,db
from marshmallow.fields import Nested
#from schemas.productschema import ProductSchema
#from schemas.priceschema import PriceGetSchema
class SizeSchema(ma.ModelSchema):
    class Meta:
        model = Sizes
        fields = ("id","hid","sizeEn","sizeAr","price","productId","isActive","taxAmount","createdAt","updatedAt")
        sqla_session = db.session

class SizeGetSchema(ma.ModelSchema):
    #product_size = ma.Nested(ProductSchema)
    #size_prices = ma.Nested(PriceGetSchema)
    class Meta:
        model =Sizes
        fields = ("id","sizeEn","sizeAr","price","productId","createdAt","updatedAt")
        sqla_session = db.session

from config import db,ma
from models.productsmodel import Products
from marshmallow.fields import Nested
from schemas.categorieschema import CategoriesSchema,CategoriesGetSchema
from schemas.sizeschema import SizeSchema,SizeGetSchema
from schemas.priceschema import PriceGetSchema
from schemas.globalsizeschema import GlobalSizeSchema

class ProductSchema(ma.ModelSchema):
    sizes              = ma.Nested(SizeGetSchema,many=True)
    class Meta:
        model = Products
        fields = ("id","hid","productEn","productAr","imagePath","isActive","sizes","categoryId","createdAt","updatedAt","descEn","descAr","modifierId","taxable")
        sqla_session = db.session


class ProductGetSchema(ma.ModelSchema):
    category = ma.Nested(CategoriesGetSchema)
    sizes              = ma.Nested(SizeGetSchema,many=True)
    globalsize_product =ma.Nested(GlobalSizeSchema)
    class Meta:
        model = Products
        fields = ("id","productEn","productAr","imagePath","isActive","categoryId","taxable","sizes",'category',"createdAt","updatedAt")
        sqla_session = db.session

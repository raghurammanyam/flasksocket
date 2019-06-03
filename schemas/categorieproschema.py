
from config import db,ma
from models.categoriesmodel import Categories
from marshmallow.fields import Nested
from schemas.productschema import ProductSchema



class CategoriesGetSchemas(ma.ModelSchema):
    products     = ma.Nested(ProductSchema,many=True)
    class Meta:
        model = Categories
        fields = ("id","categoryEn","categoryAr","imagePath","isActive","products","createdAt","updatedAt")
        sqla_session = db.session

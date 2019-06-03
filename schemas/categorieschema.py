from config import db,ma
from models.categoriesmodel import Categories
from marshmallow.fields import Nested


class CategoriesSchema(ma.ModelSchema):

    class Meta:
        model = Categories
        fields = ("id","categoryEn","categoryAr","isActive","products","imagePath","createdAt","updatedAt")
        sqla_session = db.session


class CategoriesGetSchema(ma.ModelSchema):
    class Meta:
        model = Categories
        fields = ("id","hid","categoryEn","categoryAr","imagePath","createdAt","updatedAt")
        sqla_session = db.session

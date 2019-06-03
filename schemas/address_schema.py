from config import db,ma
from models.addressmodel import Addresses
from marshmallow.fields import Nested
# from schemas.deliveryzoneschema import DeliveryzoneSchema



class AddressSchema(ma.ModelSchema):
    class Meta:
        model = Addresses
        fields = ("id","address","latitude","longitude","userId","type","createdAt","updatedAt")
        sqla_session = db.session

class AddressGetSchema(ma.ModelSchema):
    class Meta:
        model  = Addresses
        fields = ("id","address","latitude","longitude","userId","type","createdAt","updatedAt")
        sqla_session = db.session

class AddressUserSchema(ma.ModelSchema):
    class Meta:
        model = Addresses
        fields = ("id","address","latitude","longitude","userId","type","createdat","updated")
        sqla_session = db.session

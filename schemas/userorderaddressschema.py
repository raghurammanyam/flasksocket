from config import ma,db
from models.usermodel import Users
from config import ma,db
from marshmallow import fields
from marshmallow.fields import Nested
from schemas.address_schema import AddressGetSchema,AddressSchema
from schemas.ordersschema import OrderSchema
from schemas.roleschema import RoleSchema

class UserAdressSchema(ma.ModelSchema):
    Role_user  = ma.Nested(RoleSchema)
    address              = ma.Nested(AddressSchema,many=True)
    order                = ma.Nested(OrderSchema,many=True)
    class Meta:
        model = Users
        fields = ("id","name","username","mobileNumber","roleId","Role_user","address","order","createdAt","updatedAt")

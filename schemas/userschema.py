from config import ma,db
from models.rolemodel import Roles
from models.usermodel import Users
from config import ma,db
from marshmallow import fields
from marshmallow.fields import Nested
from schemas.roleschema import RoleSchema
from models.revokemodel import RevokedTokenModel
from schemas.address_schema import AddressGetSchema

class UsersGetSchema(ma.ModelSchema):
    Role_user = ma.Nested(RoleSchema)
    class Meta:
        model =Users
        fields = ("id","hid","name","loginFrom","type","roleId","Role_user","mobileNumber","username","address","createdAt","updatedAt")
        sqla_session = db.session

class UsersSchema(ma.ModelSchema):
    class Meta:
        models = Users
        fields = ("id","hid","name","loginFrom","type","roleId","mobileNumber","username","address","isActive","createdAt","updatedAt")
        sqla_session = db.session

class user_signupSchema(ma.ModelSchema):
    class Meta:
        model = Users
        fields = ("id","username","mobileNumber","address","name")
        sqla_session = db.session

class Password_ResetSchema(ma.ModelSchema):
    class Meta:
        model = Users
        fields = ("password",)
        sqla_session = db.session


class UserlogoutSchema(ma.ModelSchema):
    class Meta:
        model = RevokedTokenModel
        sqla_session = db.session

class UserOrderSchema(ma.ModelSchema):
    class Meta:
        model = Users
        fields = ("id","name","username")

class UsercountSchema(ma.ModelSchema):
    Role_user  = ma.Nested(RoleSchema)
    class Meta:
        model = Users
        fields = ("id","name","username","mobileNumber","roleId","Role_user")
class UseraccountSchema(ma.ModelSchema):
    Role_user  = ma.Nested(RoleSchema)
    class Meta:
        model = Users
        fields = ("id","name","username","mobileNumber","roleId","Role_user")


class UsersSchemas(ma.ModelSchema):
    class Meta:
        models = Users
        fields = ("id","name","mobileNumber","username","address")
        sqla_session = db.session

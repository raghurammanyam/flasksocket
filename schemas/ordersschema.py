from config import db,ma
from marshmallow import fields
from marshmallow.fields import Nested
from models.ordersmodel import Orders
from schemas.userschema import UsersGetSchema,UserOrderSchema



class OrderSchema(ma.ModelSchema):
    class Meta:
        model         = Orders
        fields        =  ("id","hid","userId","price","discount","deliveryPrice","finalPrice","orderType","orderStatus","placedOn","taxAmount","branchHid","posReference","createdAt","updatedAt")
        sqla_session  = db.session


class OrderGetSchema(ma.ModelSchema):
    user_order = ma.Nested(UserOrderSchema)
    class Meta:
        model         = Orders
        fields        = ("id","hid","deliveryPrice","discount","placedOn","userId","orderStatus","finalPrice","orderType","user_order","createdAt","updatedAt")
        sqla_session  =db.session


class OrderUserSchema(ma.ModelSchema):
    user_order = ma.Nested(UserOrderSchema)
    class Meta:
        model  = Orders
        fields = ("id","hid","userId","price","placedOn","deliveryPrice","finalPrice","user_order","branchHid","discount","orderStatus","createdAt","updatedAt")

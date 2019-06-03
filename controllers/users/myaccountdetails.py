from models.usermodel import Users
from schemas.userschema import UseraccountSchema
from config import db
from flask_restful import Resource, reqparse
from flask import request
from sqlalchemy import func
import os
from flask_jwt_extended import jwt_required
from models.ordersmodel import Orders
from models.addressmodel import Addresses
from models.rolemodel import Roles
from schemas.address_schema import AddressGetSchema
from schemas.ordersschema import OrderUserSchema


class MyAccountDetails(Resource):
    def __init__(self):
        pass
    def get(self,id):
        user = Users.query.filter(Users.id == id).one_or_none()
        user_order = db.session.query(Orders).filter(Orders.userId==id).all()
        user_address = db.session.query(Addresses).filter(Addresses.userId==id).all()
        if user is not None:
            user_schema = UseraccountSchema()
            user_data   = user_schema.dump(user).data
        else:
            pass

        if user_order is not None:
            order_schema = OrderUserSchema(many=True)
            order_data   = order_schema.dump(user_order).data
        else:
            pass
        if user_address is not None:
            address_schema = AddressGetSchema(many=True)
            address_data   = address_schema.dump(user_address).data
        else:
            pass
        return ({"success":True,"user_data":user_data,"order_data":order_data,"address_data":address_data})

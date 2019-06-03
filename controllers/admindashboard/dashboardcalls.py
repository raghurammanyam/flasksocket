from flask_restful import reqparse, abort, Api, Resource
from flask import make_response,abort,request,redirect, url_for,Flask
from config import db,app
from models.productsmodel import Products
from schemas.productschema import ProductSchema,ProductGetSchema
from sqlalchemy.orm import contains_eager ,join,joinedload,subqueryload
import os
import json
from models.usermodel import Users
from sqlalchemy import func
from models.ordersmodel import Orders
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import cast, func
from sqlalchemy.types import TIME, DATE
from sqlalchemy.sql import between
import datetime
from schemas.ordersschema import OrderSchema
from sqlalchemy import extract

class DashBoardcalls(Resource):
    def __init__(self):
        pass
    def get(self):
        try:
            productstatuscount = db.session.query(Products).order_by(Products.id).filter(Products.isActive==True).count()

            userstatuscount =  db.session.query(Users).order_by(Users.id).filter(Users.isActive==True).count()

            orderstatuscount = db.session.query(Orders).order_by(Orders.id).filter(Orders.orderStatus=="2").count()

            total_amount = (db.session.query(Users, func.sum(Orders.finalPrice)).outerjoin(Orders, Users.order).filter(Users.isActive==True,Orders.orderStatus=="2"))
            order  =  [total for b,total in total_amount]
            print(order)
            order_value =order[0]
            print(order_value)
            if (order_value == None):
                order_value = 0
            data={"productstatuscount":productstatuscount,"userstatuscount":userstatuscount,"orderstatuscount":orderstatuscount,"order_value":order_value }

            return ({"success":True,"data":data})
        except Exception as e:
                return({"success":False,"message":str(e)})

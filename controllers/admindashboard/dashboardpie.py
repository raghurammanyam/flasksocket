from flask_restful import reqparse, abort, Api, Resource
from flask import make_response,abort,request,redirect, url_for,Flask
from config import db,app
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

class DashBoardpie(Resource):
    def __init__(self):
        pass
    def get(self):
        try:
            pendingcurentorderstatus = db.session.query(Orders).order_by(Orders.id).filter(Orders.orderStatus=="1").count()

            conformedcurentorderstatus = db.session.query(Orders).order_by(Orders.id).filter(Orders.orderStatus=="2").count()

            cancelledcurentorderstatus = db.session.query(Orders).order_by(Orders.id).filter(Orders.orderStatus=="3").count()

            data={"pendingcurentorderstatus":pendingcurentorderstatus,"conformedcurentorderstatus":conformedcurentorderstatus,"cancelledcurentorderstatus":cancelledcurentorderstatus}

            return ({"success":True,"data":data,})

        except Exception as e:
                return({"success":False,"message":str(e)})

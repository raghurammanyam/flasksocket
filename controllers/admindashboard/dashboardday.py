from flask_restful import reqparse, abort, Api, Resource
from flask import make_response,abort,request,redirect, url_for,Flask
from config import db,app
from models.productsmodel import Products
from schemas.productschema import ProductSchema,ProductGetSchema
from schemas.modifierschema import ModifierSchema
from sqlalchemy.orm import contains_eager ,join,joinedload,subqueryload
from models.sizemodel import Sizes
from models.pricemodel import Prices
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
import os
import json
from sqlalchemy import func
from models.ordersmodel import Orders
from models.usermodel import Users
from config import db,basedir
#import logging, logging.config, yaml
from sqlalchemy.orm import contains_eager ,join,joinedload,subqueryload
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import cast, func
from sqlalchemy.types import TIME, DATE
from sqlalchemy.sql import between
import datetime
from schemas.ordersschema import OrderSchema
from sqlalchemy import extract
from sqlalchemy import extract
from datetime import datetime, timedelta
from datetime import date, timedelta



app = Flask(__name__,static_url_path='/static',static_folder='/python_bybloss_admin/static')
path = os.getcwd()
UPLOAD_FOLDER = path+'/static'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class DashBoardday(Resource):
    def __init__(self):
        pass
    def get(self):
            try:
                key=request.headers['key']

                if (key == "week"):

                    today = date.today()
                    weekday = today.weekday()
                    first = today - timedelta(days=weekday)
                    last = today + timedelta(days=(6 - weekday))

                    weeksum = (db.session.query(db.func.sum(Orders.finalPrice)).filter(Orders.orderStatus=="1",
                            db.func.date(Orders.createdAt)<=last,
                            db.func.date(Orders.createdAt)>=first)).all()

                    weekcount = (db.session.query(Orders).filter(Orders.orderStatus=="1",
                            db.func.date(Orders.createdAt)<=last,
                            db.func.date(Orders.createdAt)>=first)).count()
                    return ({"weekcount":weekcount,"weeksum":weeksum})

                elif(key=="today"):

                    counttoday = Orders.query.filter(Orders.orderStatus=="1",extract('day', Orders.createdAt) == datetime.today().day).count()

                    sumtoday = db.session.query(db.func.sum(Orders.finalPrice)).filter(Orders.orderStatus=="1",extract('day', Orders.createdAt) == datetime.today().day).all()

                    return ({"counttoday":counttoday,"sumtoday":sumtoday})

                elif(key == "month"):

                    countmonth = Orders.query.filter(Orders.orderStatus=="1",extract('month', Orders.createdAt) == datetime.today().month).count()

                    summonth =db.session.query(db.func.sum(Orders.finalPrice)).filter(Orders.orderStatus=="1",extract('month', Orders.createdAt) == datetime.today().month).all()

                    return ({"countmonth":countmonth,"summonth":summonth})

                elif (key == "year"):
                     countyear = Orders.query.filter(Orders.orderStatus=="1",extract('year', Orders.createdAt) == datetime.today().year).count()

                     sumyear = db.session.query(db.func.sum(Orders.finalPrice)).filter(Orders.orderStatus=="1",extract('year', Orders.createdAt) == datetime.today().year).all()
                     return ({"countyear":countyear,"sumyear":sumyear})

                else:
                    return "key is not sent in headers"

            except Exception as e:
                    return({"success":False,"message":str(e)})

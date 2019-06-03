from flask_restful import reqparse, abort, Api, Resource
from flask import make_response,abort,request,redirect, url_for,Flask
from config import db,app
from sqlalchemy.orm import contains_eager ,join,joinedload,subqueryload
import os
import json
from models.ordersmodel import Orders
from config import db,basedir
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import cast, func
from sqlalchemy.types import TIME, DATE
from sqlalchemy.sql import between
import datetime
from sqlalchemy import extract
from collections import OrderedDict
import collections





class Dashgraph(Resource):
    def __init__(self):
        pass
    def get(self):
            try:
                l=["ordermonth","ordervalue"]
                obj=db.session.query(sa.func.month(Orders.createdAt), sa.func.sum(Orders.finalPrice)).group_by(sa.func.month(Orders.createdAt)).all()
                #print(obj)
                d=dict(obj)
                for i in range(1,13):
                    if i in d.keys():
                        pass
                    else:
                        d.update({i:0})
                od = collections.OrderedDict(sorted(d.items()))
                data=dict(od)
                return ({"success":True,"data":data})
            except Exception as e:
                return({"success":False,"message":str(e)})

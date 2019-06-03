from config import db,basedir
from models.ordersmodel import Orders
from schemas.ordersschema import OrderSchema,OrderGetSchema
from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from flask import make_response,abort,request
from flask_jwt_extended import jwt_required

import os

import logging, logging.config, yaml


CONFIG_PATH = os.path.join(basedir,'loggeryaml/orderslogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('postorders')
loggers = logging.getLogger("consoleorders")




class PostOrders(Resource):
    def __init__(self):
        pass
    #@jwt_required
    def post(self):
        try:
            order = request.get_json()
            schema = OrderSchema()
            new_order = schema.load(order,db.session).data
            db.session.add(new_order)
            db.session.commit()

            data = schema.dump(new_order).data

            logger.info("data posted successfully")
            loggers.info("data posted successfully")
            return ({"success":True,"data":data})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})

    def get(self):
        try:

            order_data = db.session.query(Orders).order_by(Orders.id).all()
            if order_data:
                schema = OrderGetSchema(many=True)
                data   = schema.dump(order_data).data
                logger.info("data feteched successfully")
                loggers.info("data feteched successfully")
                return ({"success":True,"data":data})
            else:
                logger.warning("data not availiable for orders")
                loggers.warning("data not availiable for orders")
                return ({"success":False,"message":"data not availiable for orders"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})

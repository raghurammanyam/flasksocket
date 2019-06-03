from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from flask import make_response,abort,request
from config import db,basedir
from models.ordersmodel import Orders
from schemas.ordersschema import OrderGetSchema,OrderSchema,OrderUserSchema
from flask_jwt_extended import jwt_required
import os

from config import db,basedir
import logging, logging.config, yaml


CONFIG_PATH = os.path.join(basedir,'loggeryaml/orderslogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('getupdateorders')
loggers = logging.getLogger("consoleorders")


class OrderById(Resource):
    def __init__(self):
        pass

    def get(self,id):
        try:
            order=db.session.query(Orders).filter(Orders.id==id).first()
            if order:
                schema = OrderGetSchema()
                data = schema.dump(order).data
                logger.info("data fetched based on id ")
                loggers.info("data fetched based on id ")
                return ({"success":True,"data":data})
            else:
                logger.warning("no data found on this id")
                loggers.warning("no data found on this id")
                return ({"success":False,"message":"no data found on this id"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})
    #@jwt_required
    def put(self,id):
        try:
            order=db.session.query(Orders).filter(Orders.id==id).update(request.get_json())
            if order:
                db.session.commit()
                order_detail=db.session.query(Orders).filter_by(id=id).one()
                schema = OrderSchema()
                data = schema.dump(order_detail).data
                logger.info("data updated successfully")
                loggers.info("data updated successfully")
                return({"success":True,"data":data})
            else:
                logger.warning("order data not updated")
                loggers.warning("order data not updated")
                return({"success":False,"message":"order data not updated"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})

    def delete(self,id):
       try:
            order=db.session.query(Orders).filter(Orders.id==id).first()
            if order:
                db.session.delete(order)
                db.session.commit()
                logger.info("order deleted successfully ")
                loggers.info("order deleted successfully ")
                return({"success":True,"message":"order deleted successfully"})
            else:
                logger.warning("order not deleted on this id")
                loggers.warning("order not deleted on this id")
                return({"success":False,"message":"order not deleted on this id"})
       except Exception as e:
           logger.warning(str(e))
           loggers.warning(str(e))
           return({"success":False,"message":str(e)})





class OrderByuser(Resource):
    def __init__(self):
        pass
    def get(self,id):
        try:
            order=db.session.query(Orders).filter(Orders.userId==id).all()
            if order:
                schema = OrderUserSchema(many=True)
                data = schema.dump(order).data
                logger.info("data feteched successfully")
                loggers.info("data feteched successfully")
                return ({"success":True,"data":data})
            else:
                logger.warning("no orderdata found on this userid")
                loggers.warning("no orderdata found on this userid")
                return ({"success":False,"message":"no data found on this userid"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})

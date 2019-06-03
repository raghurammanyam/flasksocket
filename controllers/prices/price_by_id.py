from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from flask import make_response,abort,request
from config import db
from models.pricemodel import Prices
from schemas.priceschema import PriceGetSchema,PriceSchema
from schemas.productschema import ProductGetSchema


import os
import logging, logging.config, yaml
from config import db,basedir
CONFIG_PATH = os.path.join(basedir,'loggeryaml/pricelogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('getupdateprices')
loggers = logging.getLogger("consoleprices")





class PriceByID(Resource):
    def __init__(self):
        pass
    def get(self,id):
        try:
            price=db.session.query(Prices).filter(Prices.id==id).first()
            if price:
                schema = PriceGetSchema()
                data = schema.dump(price).data
                logger.info("data fetched succesffully based on id ")
                loggers.info("data fetched succesffully based on id ")
                return ({"success":True,"data":data})
            else:
                logger.warning("no data found on this id")
                loggers.warning("no data found on this id")
                return ({"success":False,"message":"no data found on this id"})

        except:
            logger.warning("no data found on this id")
            loggers.warning("no data found on this id")
            return ({"success":False,"message":"no data found on this id"})

    def put(self,id):
        try:
            price=db.session.query(Prices).filter(Prices.id==id).update(request.get_json())
            if price:
                db.session.commit()
                price_detail=db.session.query(Prices).filter_by(id=id).one()
                schema = PriceSchema()
                data = schema.dump(price_detail).data
                logger.info("data updated  succesffully based on id ")
                loggers.info("data updated succesffully based on id ")
                return({"success":True,"data":data})
            else:
                logger.warning("price data not updated")
                loggers.warning("price data not updated")
                return({"success":False,"message":"price data not updated"})
        except:
            logger.warning("price data not updated")
            loggers.warning("price data not updated")
            return({"success":False,"message":"price data not updated"})


    def delete(self,id):
        try:
            price=db.session.query(Prices).filter(Prices.id==id).first()
            if price:
                db.session.delete(price)
                db.session.commit()
                return({"success":True,"message":"price deleted successfully"})
            else:
                return({"success":False,"message":"price not deleted on this id"})
        except:
            return({"success":False,"message":"price not deleted on this id"})

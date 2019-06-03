from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from flask import make_response,abort,request
from config import db
from models.pricemodel import Prices
from schemas.priceschema import PriceGetSchema,PriceSchema
from schemas.productschema import ProductGetSchema
from schemas.sizeschema import SizeSchema,SizeGetSchema
import os
import logging, logging.config, yaml
from config import db,basedir

CONFIG_PATH = os.path.join(basedir,'loggeryaml/pricelogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('postprices')
loggers = logging.getLogger("consoleprices")


class PostPrices(Resource):
    def __init__(self):
        pass
    def get(self):
        try:
            obj=db.session.query(Prices).order_by(Prices.id).all()
            if obj:
                schema = PriceGetSchema(many=True)
                data   = schema.dump(obj).data
                logger.info("data feteched succesffully")
                loggers.info("data feteched succesffully")
                return ({"success":True,"data":data})
            else:
                logger.warning("No data is available for prices")
                loggers.warning("No data is available for prices")
                return({"success":False,"message":"No data is available for prices"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})


    def post(self):
        try:
            da = request.get_json()
            price_prodID= da['productId']
            print(da)
            existing_priceid = (Prices.query.filter(Prices.productId == price_prodID).one_or_none())
            if existing_priceid is None:
                schema= PriceSchema()
                new_price = schema.load(da, db.session).data
                print(new_price.__dict__)
                db.session.add(new_price)
                db.session.commit()
                data = schema.dump(new_price).data
                logger.info("data posted succesffully")
                loggers.info("data posted succesffully")
                return ({"success":True,"data":data})
            else:
                logger.warning("price exists already")
                loggers.warning("price exists already")
                return({"success":False,"message":"price exists already"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})

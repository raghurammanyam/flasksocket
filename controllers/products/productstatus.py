from datetime import datetime
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
from schemas.sizeschema import SizeSchema
import json


from config import db,basedir
import logging, logging.config, yaml


CONFIG_PATH = os.path.join(basedir,'loggeryaml/productslogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('getproductsizes')
loggers = logging.getLogger("consoleproducts")



class GetProductSizeStatus(Resource):
    def __init__(self):
        pass
    def get(self):
        try:
            obj = db.session.query(Products).join(Products.sizes).options(contains_eager(Products.sizes)).filter(Sizes.isActive == True)
            if obj:
                schema = ProductGetSchema(many=True)
                data   = schema.dump(obj).data
                logger.info("data fetched successfully")
                loggers.info("data fetched successfully")
                return ({"success":True,"data":data})
            else:
                logger.warning("No data is available for products")
                loggers.warning("No data is available for products")
                return({"success":False,"message":"No data is available for products"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})

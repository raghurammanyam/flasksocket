from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from flask import make_response,abort,request,redirect, url_for,Flask
from config import db,app,ROOT_DIR,basedir
from werkzeug.utils import secure_filename
from models.addressmodel import Addresses
from schemas.address_schema import AddressSchema,AddressGetSchema
import os
from sqlalchemy import desc
from flask_jwt_extended import jwt_required
from config import db,basedir
import logging, logging.config, yaml


CONFIG_PATH = os.path.join(basedir,'loggeryaml/addresslogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('postaddresss')
loggers = logging.getLogger('consoleaddresss')





class PostAddress(Resource):
    def __init__(self):
        pass
    #@jwt_required
    def post(self):
        #try:
            address = request.get_json()
            name = address['address']
            id   = address['userId']
            existing_address = (Addresses.query.filter(Addresses.address == name).filter(Addresses.userId==id).one_or_none())
            if existing_address is None:
                schema = AddressSchema()
                new_address = schema.load(address, session=db.session).data
                db.session.add(new_address)
                db.session.commit()
                data = schema.dump(new_address).data
                logger.info("data posted successfully")
                loggers.info("data posted successfully")
                return ({"success":True,"data":data})
            else:
                logger.warning("address exists already")
                loggers.warning("address exists already")
                return({"success":False,"message":"address exists already"})
        #except Exception as e:
            #logger.warning(str(e))
            #loggers.warning(str(e))
            #return({"success":False,"message": str(e)})

    def get(self):
        try:
            address=db.session.query(Addresses).order_by(desc(Addresses.createdAt)).all()
            if address:
                schema      = AddressGetSchema(many=True)
                data        = schema.dump(address).data
                logger.info("data feteched successfully")
                loggers.info("data feteched successfully")
                return ({"success":True,"data":data})
            else:
                logger.warning("No data is available for address")
                loggers.warning("No data is available for address")
                return({"success":False,"message":"No data is available for address"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})

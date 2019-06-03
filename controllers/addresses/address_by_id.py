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
import logging, logging.config, yaml


CONFIG_PATH = os.path.join(basedir,'loggeryaml/addresslogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('getupdateaddresss')
loggers = logging.getLogger('consoleaddresss')



class AdressByID(Resource):
    def __init__(self):
        pass
    def get(self,id):
        try:
            address=db.session.query(Addresses).filter(Addresses.id==id).first()
            if address:
                schema = AddressGetSchema()
                data = schema.dump(address).data
                logger.info("data feteched successfully based on id ")
                loggers.info("data feteched successfully based on id ")
                return ({"success":True,"data":data})
            else:
                logger.warning("no data found on this id")
                loggers.warning("no data found on this id")
                return ({"success":False,"message":"no data found on this id"})

        except Exception as e:
            logger.warning( str(e))
            loggers.warning( str(e))
            return({"success":False,"message": str(e)})
    @jwt_required
    def put(self,id):
        try:
            address=db.session.query(Addresses).filter(Addresses.id==id).update(request.get_json())
            if address:
                db.session.commit()
                address_detail=db.session.query(Addresses).filter_by(id=id).one()
                schema = AddressSchema()
                data = schema.dump(address_detail).data
                logger.info("data updated successfully based on id ")
                loggers.info("data updated successfully based on id ")
                return({"success":True,"data":data})
            else:
                logger.warning("address data not updated")
                loggers.warning("address data not updated")
                return({"success":False,"message":"address data not updated"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message": str(e)})


    def delete(self,id):
        try:
            address=db.session.query(Addresses).filter(Addresses.id==id).first()
            if address:
                db.session.delete(address)
                db.session.commit()
                logger.info("address deleted successfully ")
                loggers.info("address deleted successfully ")
                return({"success":True,"message":"address deleted successfully"})
            else:
                logger.warning("address not deleted on this id")
                loggers.warning("address not deleted on this id")
                return({"success":False,"message":"address not deleted on this id"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message": str(e)})

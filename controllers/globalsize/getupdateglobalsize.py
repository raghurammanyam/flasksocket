from datetime import datetime
from flask import make_response,abort,request
from models.globalsizemodel import GlobalSizes
from schemas.globalsizeschema import GlobalSizeSchema
from flask_restful import reqparse, abort, Api, Resource
import os
from config import db,basedir
import logging, logging.config, yaml


CONFIG_PATH = os.path.join(basedir,'loggeryaml/globalsizelogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('getupdateglobalsizes')
loggers = logging.getLogger("consoleglobalsizes")


class GetUpdateDeleteGlobalSize(Resource):
    def __init__(self):
        pass
    def get(self,id):
        try:
            obj=db.session.query(GlobalSizes).filter(GlobalSizes.id==id).first()
            if obj:
                globalsize_schema = GlobalSizeSchema()
                data = globalsize_schema.dump(obj).data
                logger.info("Data feteched successfully based on id ")
                loggers.info("Data feteched successfully based on id ")
                return({"success":True,"data":data})
            else:
                logger.warning("golbalsize id  not found")
                loggers.warning("golbalsize id  not found")
                return({"success":False,"message": "golbalsize id  not found"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})


    # call to update the GlobalSizes based on id
    def put(self,id):
        try:
            global_sizes =request.get_json()
            sizeEn=global_sizes['sizeEn']
            existing_globalsize = (GlobalSizes.query.filter(GlobalSizes.sizeEn == sizeEn).all())
            if existing_globalsize is None:
                obj=db.session.query(GlobalSizes).filter(GlobalSizes.id==id).update(request.get_json())
                if obj:
                    db.session.commit()
                    abc=db.session.query(GlobalSizes).filter_by(id=id).one()
                    schema = GlobalSizeSchema()
                    data = schema.dump(abc).data
                    logger.info("Data updated successfully based on id ")
                    loggers.info("Data updated successfully based on id ")
                    return({"success":True,"data":data})
                else:
                    logger.warning("size not updated")
                    loggers.warning("size not updated")
                    return({"success":False,"message": "size not updated"}  )
            else:
                logger.warning("size already exists")
                loggers.warning("size already exists")
                return({"success":False,"message": "size already exists"}  )
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})



    # call to delete the Globalsizes based on id
    def delete(self,id):
        try:
            obj=db.session.query(GlobalSizes).filter(GlobalSizes.id==id).first()
            if obj:
                db.session.delete(obj)
                db.session.commit()
                logger.info("succesffully deleted")
                loggers.info("succesffully deleted")
                return({"success":True,"message":"succesffully deleted"})
            else:
                logger.warning("Globalsize doesnot deleted")
                loggers.warning("Globalsize doesnot deleted")
                return({"success":False,"message": "Globalsize doesnot deleted "})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})

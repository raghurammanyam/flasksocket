from datetime import datetime
from flask import make_response,abort,request
from models.sizemodel import Sizes
from schemas.sizeschema import SizeSchema, SizeGetSchema
from config import db
from flask_restful import reqparse, abort, Api, Resource
import os



from config import db,basedir
import logging, logging.config, yaml


CONFIG_PATH = os.path.join(basedir,'loggeryaml/sizelogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('getupdatesizes')
loggers = logging.getLogger("consolesizes")



class GetUpdateDeleteSizes(Resource):
    def __init__(self):
        pass
    def get(self,id):
        try:
            obj=db.session.query(Sizes).filter(Sizes.id==id).first()
            if obj:
                role_schema = SizeSchema()
                data = role_schema.dump(obj).data
                logger.info("data feteched successfully")
                loggers.info("data feteched successfully")
                return({"success":True,"data":data})
            else:
                logger.warning("sizes not found")
                loggers.warning("sizes not found")
                return({"success":False,"message": "sizes not found"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})


    def put(self,id):
        try:
            obj=db.session.query(Sizes).filter(Sizes.id==id).update(request.get_json())
            if obj:
                db.session.commit()
                abc=db.session.query(Sizes).filter_by(id=id).one()
                schema = SizeSchema()
                data = schema.dump(abc).data
                logger.info("data updated successfully")
                loggers.info("data updated successfully")
                return({"success":True,"data":data})
            else:
                logger.warning("size not updated")
                loggers.warning("size not updated")
                return({"success":False,"message": "size not updated"}  )
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})




    def delete(self,id):
        try:
            obj=db.session.query(Sizes).filter(Sizes.id==id).first()
            if obj:
                db.session.delete(obj)
                db.session.commit()
                logger.info("succesffully deleted")
                loggers.info("succesffully deleted")
                return({"success":True,"message":"succesffully deleted"})
            else:
                logger.warning("size doesnot deleted")
                loggers.warning("size doesnot deleted")
                return({"success":False,"message": "size doesnot deleted "})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})

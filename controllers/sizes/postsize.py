from datetime import datetime
from flask import make_response,abort,request
from models.sizemodel import Sizes
from schemas.sizeschema import SizeSchema,SizeGetSchema
from config import db
from flask_restful import reqparse, abort, Api, Resource
import os



from config import db,basedir
import logging, logging.config, yaml


CONFIG_PATH = os.path.join(basedir,'loggeryaml/sizelogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('postsizes')
loggers = logging.getLogger("consolesizes")




class Getcreatesize(Resource):
    def __init__(self):
        pass

    def get(self):
        try:
            obj=db.session.query(Sizes).order_by(Sizes.id).all()
            if obj:
                size_schema = SizeGetSchema(many=True)
                data = size_schema.dump(obj).data
                logger.info("data feteched successfully")
                loggers.info("data feteched successfully")
                return({"success":True,"data":data})

            else:
                logger.warning("Sizes not found")
                loggers.warning("Sizes not found")
                return({"success":False,"message": "Sizes not found"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})



    def post(self):
        try:
            da = request.get_json()
            sizeEn = da['sizeEn']
            existing_size = (Sizes.query.filter(Sizes.sizeEn == sizeEn).one_or_none())
            if existing_size is None:
                schema = SizeSchema()
                new_size = schema.load(da, session=db.session).data
                db.session.add(new_size)
                db.session.commit()
                data = schema.dump(new_size).data
                logger.info("data posted successfully")
                loggers.info("data posted successfully")
                return({"success":True,"data":data})
            else:
                logger.warning("Size name exists already")
                loggers.warning("Size name exists already")
                return({"success":False,"message":"Size name exists already"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})

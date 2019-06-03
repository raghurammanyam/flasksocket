from datetime import datetime
from flask import make_response,abort,request
from models.globalsizemodel import GlobalSizes
from schemas.globalsizeschema import GlobalSizeSchema
from config import db,basedir
from flask_restful import reqparse, abort, Api, Resource
import os

import logging, logging.config, yaml


CONFIG_PATH = os.path.join(basedir,'loggeryaml/globalsizelogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('postglobalsizes')
loggers = logging.getLogger("consoleglobalsizes")


class GetcreateGlobalSize(Resource):
    def __init__(self):
        pass
    # globalsizes get call
    def get(self):
        try:
            obj=db.session.query(GlobalSizes).order_by(GlobalSizes.id).all()
            if obj:
                globalsize_schema = GlobalSizeSchema(many=True)
                data = globalsize_schema.dump(obj).data
                logger.info("data feteched succesffully")
                loggers.info("data feteched succesffully")
                return({"success":True,"data":data})
            else:
                logger.warning("globalsize not found")
                loggers.warning("globalsize not found")
                return({"success":False,"message": "globalsize not found"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})


    # global sizes post call

    def post(self):
        try:
            size_list=[]
            da = request.get_json()
            obj=da["globalsizes"]
            for x in obj:
                sizeEn = x['sizeEn']
                existing_globalsize = (GlobalSizes.query.filter(GlobalSizes.sizeEn == sizeEn).one_or_none())
                if existing_globalsize is None:
                    schema = GlobalSizeSchema()
                    new_globalsize = schema.load(x, session=db.session).data
                    db.session.add(new_globalsize)
                    db.session.commit()
                    data = schema.dump(new_globalsize).data
                    size_list.append(data)
                else:
                    return ({"success":False,"message":"size already exists"})
                return({"success":True,"data":size_list})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})

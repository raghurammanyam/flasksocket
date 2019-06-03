from datetime import datetime
from flask import make_response,abort,request
from models.rolemodel import Roles
from schemas.roleschema import RoleSchema
from config import db
from flask_restful import reqparse, abort, Api, Resource
import os



from config import db,basedir
import logging, logging.config, yaml


CONFIG_PATH = os.path.join(basedir,'loggeryaml/roleslogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('postroles')
loggers = logging.getLogger("consoleroles")


class Getcreateroles(Resource):
    def __init__(self):
        pass
    # Roles get call
    def get(self):
        try:
            role=db.session.query(Roles).order_by(Roles.id).all()
            if role:
                role_schema = RoleSchema(many=True)
                data = role_schema.dump(role).data
                logger.info("data feteched successfully")
                loggers.info("data feteched successfully")
                return({"success":True,"data":data})
            else:
                logger.warning("roles not found")
                loggers.warning("roles not found")
                return({"success":False,"message": "roles not found"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})


    def post(self):
        try:
            da = request.get_json()
            name = da['role']
            existing_role = (Roles.query.filter(Roles.role == name).one_or_none())
            if existing_role is None:
                schema = RoleSchema()
                new_role = schema.load(da, session=db.session).data
                db.session.add(new_role)
                db.session.commit()
                data = schema.dump(new_role).data
                logger.info("data posted successfully")
                loggers.info("data posted successfully")
                return({"success":True,"data":data})
            else:
                logger.warning("Role name exists already")
                loggers.warning("Role name exists already")
                return("Role name exists already")
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})

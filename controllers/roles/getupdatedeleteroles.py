from datetime import datetime
from flask import make_response,abort,request
from models.rolemodel import Roles
from schemas.roleschema import RoleSchema, RolesGetSchema
from config import db
from flask_restful import reqparse, abort, Api, Resource
import os


from config import db,basedir
import logging, logging.config, yaml


CONFIG_PATH = os.path.join(basedir,'loggeryaml/roleslogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('getupdateroles')
loggers = logging.getLogger("consoleroles")



class GetUpdateDeleteRoles(Resource):
    def __init__(self):
        pass
    def get(self,id):
        try:
            role=db.session.query(Roles).filter(Roles.id==id).first()
            if role:
                role_schema = RoleSchema()
                data = role_schema.dump(role).data
                logger.info("data feteched successfully baesd on id ")
                loggers.info("data feteched successfully baesd on id ")
                return({"success":True,"data":data})
            else:
                logger.warning("roles not found")
                loggers.warning("roles not found")
                return({"success":False,"message": "roles not found"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})


    # call to update the role based on id
    def put(self,id):
        try:
            da = request.get_json()
            name = da['role']
            existing_role = (Roles.query.filter(Roles.role == name).one_or_none())
            if existing_role is None:
                obj=db.session.query(Roles).filter(Roles.id==id).update(request.get_json())
                if obj:
                    db.session.commit()
                    abc=db.session.query(Roles).filter_by(id=id).one()
                    schema = RoleSchema()
                    data = schema.dump(abc).data
                    logger.info("data updated successfully baesd on id ")
                    loggers.info("data updated successfully baesd on id ")
                    return({"success":True,"data":data})
                else:
                    logger.warning("role not updated")
                    loggers.warning("role not updated")
                    return({"success":False,"message": "role not updated"}  )
            else:
                logger.warning("Role name exists already")
                loggers.warning("Role name exists already")
                return("Role name exists already")
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})

    # call to delete the role based on id
    def delete(self,id):
        try:
            obj=db.session.query(Roles).filter(Roles.id==id).first()
            if obj:
                db.session.delete(obj)
                db.session.commit()
                logger.info("succesffully deleted ")
                loggers.info("succesffully deleted")
                return({"success":True,"message":"succesffully deleted"})
            else:
                logger.warning("role doesnot deleted")
                loggers.warning("role doesnot deleted")
                return({"success":False,"message": "role doesnot deleted "})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})

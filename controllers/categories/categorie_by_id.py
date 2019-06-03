from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from flask import make_response,abort,request,Flask,url_for
from config import db,app
from models.categoriesmodel import Categories
from schemas.categorieschema import CategoriesSchema
from werkzeug.utils import secure_filename
import os
from flask_jwt_extended import jwt_required
from config import db,basedir
import logging, logging.config, yaml
from schemas.categorieproschema import CategoriesGetSchemas
from schemas.categorieproschema import CategoriesGetSchemas

CONFIG_PATH = os.path.join(basedir,'loggeryaml/categorielogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('getupdatecategories')
loggers = logging.getLogger('consolepostcategories')



app = Flask(__name__,static_url_path='/static',static_folder='/python_bybloss_admin/static')
path = os.getcwd()
UPLOAD_FOLDER = path+'/static'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class IdByCategorie(Resource):
    def __init__(self):
        pass

    #@jwt_required
    def get(self,id):
        try:
            categorie=db.session.query(Categories).filter(Categories.id==id).first()
            if categorie:
                schema = CategoriesGetSchemas()
                data = schema.dump(categorie).data
                print(">>>>>>>>>>>>>>>>",data)
                logger.info("Data fetched successfully based on id ")
                loggers.info("Data fetched successfully based on id")
                return ({"success":True,"data":data})
            else:
                logger.warning("No data found on this id")
                loggers.warning("No data found on this id")
                return ({"success":False,"message":"No data found on this id"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})

    #@jwt_required
    def put (self,id):
        try:
            categorie_data = request.form.to_dict()
            if 'isActive' in categorie_data.keys():
                status=categorie_data['isActive']
                categorie_data['isActive'] = int(status)
            print(categorie_data,"......")
            if 'file' not in request.files:
                imagepath = ''
            elif 'file' in request.files:
                file =request.files['file']
                if file.filename == '':
                    imagepath = ''
                if file :
                    def image():
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        return url_for("static",filename=filename)
                    imagepath = image()
            if  imagepath != '':
                categorie_data['imagePath'] = imagepath
            print(categorie_data,"....")
            category=db.session.query(Categories).filter(Categories.id==id).update(categorie_data)
            print(category,"db check")
            if category:
                db.session.commit()
                categorie_detail=db.session.query(Categories).filter_by(id=id).one()
                print(categorie_detail.__dict__)
                schema = CategoriesGetSchemas()
                data = schema.dump(categorie_detail).data
                logger.info("Data updated successfully based on id ")
                loggers.info("Data updated successfully based on id")
                return({"success":True,"data":data})
            else:
                logger.warning("Category data not updated")
                loggers.warning("Category data not updated")
                return({"success":False,"message":"Category data not updated"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})


    def delete(self,id):
            try:
                categorie=db.session.query(Categories).filter(Categories.id==id).first()
                if categorie:
                    db.session.delete(categorie)
                    db.session.commit()
                    logger.info("Category deleted successfully")
                    loggers.info("Category deleted successfully")
                    return({"success":True,"message":"Category deleted successfully"})
                else:
                    logger.warning("Category not deleted on this id")
                    loggers.warning("Category not deleted on this id")
                    return({"success":False,"message":"Category not deleted on this id"})
            except Exception as e:
                logger.warning(str(e))
                loggers.warning(str(e))
                return({"success":False,"message":str(e)})

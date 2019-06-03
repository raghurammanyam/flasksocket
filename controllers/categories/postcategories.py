from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from flask import make_response,abort,request,redirect, url_for,Flask
from config import db,app,ROOT_DIR
from werkzeug.utils import secure_filename
from models.categoriesmodel import Categories
from schemas.categorieschema import CategoriesSchema,CategoriesGetSchema
import os
from sqlalchemy import desc
from flask_jwt_extended import jwt_required
from schemas.categorieproschema import CategoriesGetSchemas
from config import db,basedir,socketio
import logging, logging.config, yaml

CONFIG_PATH = os.path.join(basedir,'loggeryaml/categorielogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('postcategories')
loggers = logging.getLogger("consolepostcategories")



app = Flask(__name__,static_url_path='/static',static_folder='/python_bybloss_admin/static')
path = os.getcwd()
UPLOAD_FOLDER = path+'/static'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class CategoriesPost(Resource):
    def __init__(self):
        pass

    #@jwt_required
    def get(self):
        try:

            categories=db.session.query(Categories).order_by(desc(Categories.createdAt)).all()
            if categories:
                schema      = CategoriesGetSchemas(many=True)
                data        = schema.dump(categories).data
                logger.info("Data feteched successfully of the category")
                loggers.info("Data feteched successfully of the category")
                socketio.emit('someevent', {'data': data})
                return ({"success":True,"data":data})
            else:
                logger.warning("No data is available for category")
                loggers.warning("No data is available for category")
                socketio.emit('someevent', {'data': "data"})
                return({"success":False,"message":"No data is available for category"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})

    def post(self):
        try:
            categorie = request.form.to_dict()
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
            name = categorie['categoryEn']
            abc ={key:value for key,value in categorie.items()}
            if  imagepath != '':
                abc['imagePath']=imagepath
            existing_categorie = (Categories.query.filter(Categories.categoryEn == name).one_or_none())
            if existing_categorie is None:
                schema = CategoriesSchema()
                new_categorie = schema.load(abc, session=db.session).data
                db.session.add(new_categorie)
                db.session.commit()
                data = schema.dump(new_categorie).data
                logger.info("Data posted successfully to the category")
                loggers.info("Data posted successfully to the category")
                socketio.emit('somecategorie', {'data': data})
                return ({"success":True,"data":data})
            else:
                logger.warning("Category exists already")
                loggers.warning("Category exists already")
                return ({"success":False,"message":"Category exists already"})
        except Exception as e:
           logger.warning(str(e))
           return({"success":False,"message":str(e)})


class CategoriesSearch(Resource):
    def __init__(self):
        pass

    def post(self):
        try:
            category_name = request.get_json()['categoryEn']
            if category_name:
                existing_categorie = (Categories.query.filter(Categories.categoryEn == category_name).all())
                if existing_categorie:
                    return({"success": True,"message":"Category exists already"})
                else:
                    return({"success": False,"message":"Category Doesnot Exists"})
            return({"message":"Please enter something"})
        except Exception as e:
            logger.warning(str(e))
            return({"success":False,"message":str(e)})

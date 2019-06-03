from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from flask import make_response,abort,request,redirect, url_for,Flask
from config import db,app
from models.productsmodel import Products
from schemas.productschema import ProductSchema,ProductGetSchema
from schemas.modifierschema import ModifierSchema
from sqlalchemy.orm import contains_eager ,join,joinedload,subqueryload
from models.sizemodel import Sizes
from models.pricemodel import Prices
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
import os
from schemas.sizeschema import SizeSchema
import json
from models.categoriesmodel import Categories

from config import db,basedir
import logging, logging.config, yaml


CONFIG_PATH = os.path.join(basedir,'loggeryaml/productslogger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH),Loader=yaml.FullLoader))
logger = logging.getLogger('postproducts')
loggers = logging.getLogger("consoleproducts")


app = Flask(__name__,static_url_path='/static',static_folder='/python_bybloss_admin/static')
path = os.getcwd()
UPLOAD_FOLDER = path+'/static'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class ProductsPost(Resource):
    def __init__(self):
        pass
    #@jwt_required
    def get(self):

        try:
            obj = db.session.query(Products).order_by(Products.id).all()
            objs = db.session.query(Products).join(Products.category).options(contains_eager(Products.category)).filter(Categories.isActive == True)
            if obj:
                schema = ProductGetSchema(many=True)
                data   = schema.dump(objs).data
                logger.info("data fetched successfully")
                loggers.info("data fetched successfully")
                return ({"success":True,"data":data})
            else:
                logger.warning("No data is available for products")
                loggers.warning("No data is available for products")
                return({"success":False,"message":"No data is available for products"})
        except Exception as e:
            logger.warning(str(e))
            loggers.warning(str(e))
            return({"success":False,"message":str(e)})

    def post(self):
        try:
            product = request.form.to_dict()
            print(product)
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
            productEn = product['productEn']
            abc ={key:value for key,value in product.items() if key!='sizes' if key!='file'}
            print(abc)
            if  imagepath != '':
                abc['imagePath']=imagepath
            existing_product = (Products.query.filter(Products.productEn == productEn).one_or_none())
            if existing_product is None:
                schema= ProductSchema()
                new_product = schema.load(abc, db.session).data
                db.session.add(new_product)
                db.session.commit()
                data = schema.dump(new_product).data
                if 'sizes' in product.keys():
                    #print("type",type(product['sizes']))
                    sizes =json.loads(product['sizes'])
                    product_id=data['id']
                    for x in sizes:
                        print("sizes:",x)
                        name = x['sizeEn']
                        x['productId']=product_id
                        size_new = {key:value for key,value in x.items()}
                        existing_size = (Sizes.query.filter(Sizes.sizeEn == name).filter(Sizes.productId==product_id).one_or_none())
                        if existing_size is None:
                            schema_size= SizeSchema()
                            new_size = schema_size.load(size_new, db.session).data
                            db.session.add(new_size)
                            db.session.commit()
                logger.info("data posted successfully")
                loggers.info("data posted successfully")
                return ({"success":True,"data":data})
            else:
                logger.warning("product exists already")
                loggers.warning("product exists already")
                return ({"success":False,"message":"product exists already"})
        except Exception as e:
            logger.warning(str(e))
            return({"success":False,"message":str(e)})


class ProductSearch(Resource):
    def __init__(self):
        pass

    def post(self):
        try:
            Product_name = request.get_json()['productEn']
            if Product_name:
                existing_product = (Products.query.filter(Products.productEn == Product_name).all())
                if existing_product:
                    logging.info("Product exists already")
                    return({"success": True,"message":"Product exists already"})
                else:
                    logging.warning("Product Doesnot Exists")
                    return({"success": False,"message":"Product Doesnot Exists"})
            logging.warning("Please enter something")
            return({"message":"Please enter something"})
        except Exception as e:
            logger.warning(str(e))
            return({"success":False,"message":str(e)})

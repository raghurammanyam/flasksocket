from flask import Flask
import os
from config import db,app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models.addressmodel import *
from models.categoriesmodel import *
# from models.deliveryzonesmodel import *
from models.globalsizemodel import *
from models.modifiersmodel import *
from models.ordersmodel import *
from models.pricemodel import *
from models.productsmodel import *
from models.revokemodel import *
from models.rolemodel import *
from models.sizemodel import *
from models.usermodel import *



app.config.from_object(os.environ['APP_SETTINGS'])

print(os.environ['APP_SETTINGS'])


migrate = Migrate(app, db)

app.app_context().push()

db.init_app(app)
db.create_all(app=app)
db.session.commit()

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()

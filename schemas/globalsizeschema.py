from config import ma,db
from models.globalsizemodel import  GlobalSizes


class GlobalSizeSchema(ma.ModelSchema):
    class Meta:
        model = GlobalSizes
        sqla_session = db.session

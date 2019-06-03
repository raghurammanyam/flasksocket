from models.rolemodel import Roles
from config import ma,db


class RoleSchema(ma.ModelSchema):
    class Meta:
        model = Roles
        fields = ("id","role","createdAt","updatedAt")
        sqla_session = db.session

class RolesGetSchema(ma.ModelSchema):
    class Meta:
        model = Roles
        sqla_session = db.session

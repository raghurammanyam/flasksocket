
from config import ma,db
from models.modifiersmodel import Modifiers


class ModifierSchema(ma.ModelSchema):
    class Meta:
        model = Modifiers
        sqla_session = db.session

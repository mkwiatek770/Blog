from settings.ma import ma
from models import TagModel


class TagSchema(ma.ModelSchema):
    class Meta:
        model = TagModel
        dump_only = ("id",)

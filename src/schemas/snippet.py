from settings.ma import ma
from models import SnippetModel
from schemas.tag import TagSchema


class SnippetSchema(ma.ModelSchema):
    tags = ma.Nested(TagSchema, many=True)

    class Meta:
        model = SnippetModel
        dump_only = ("id",)

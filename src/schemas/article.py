from marshmallow import fields
from settings.ma import ma
from models.article import ArticleModel
from schemas.tag import TagSchema


class ArticleSchema(ma.ModelSchema):

    tags = ma.Nested(TagSchema, many=True)

    class Meta:
        model = ArticleModel
        dump_only = ("id",)
        include_fk = True
        ordered = True

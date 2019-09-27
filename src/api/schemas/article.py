from marshmallow import fields
from settings.ma import ma
from models.article import ArticleModel
from schemas.tag import TagSchema
from schemas.article_content import ContentSchema


class ArticleSchema(ma.ModelSchema):

    tags = ma.Nested(TagSchema, many=True)
    content = ma.Nested(ContentSchema, many=True)

    class Meta:
        model = ArticleModel
        dump_only = ("id",)
        include_fk = True
        ordered = True

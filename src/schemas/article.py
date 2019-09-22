from settings.ma import ma
from models.article import ArticleModel


class ArticleSchema(ma.ModelSchema):
    class Meta:
        model = ArticleModel
        # load_only = ("")
        dump_only = ("id",)

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models import ArticleModel
from schemas.article import ArticleSchema

article_schema = ArticleSchema()
article_schema_many = ArticleSchema(many=True)


class PublishedArticles(Resource):

    @classmethod
    def get(cls):
        published_articles = ArticleModel.find_all()
        return article_schema_many.dump(published_articles), 200

    @classmethod
    def post(cls):
        # article_json = request.get_json()
        # article_data = article_schema.load(article_json)
        # if ArticleModel.find_by_title(article_json["title"]):
        #     return {"message": "Article already exists"}

        # article = ArticleModel()
        # article.title
        pass


class UnpublishedArticles(Resource):

    @classmethod
    @jwt_required
    def get(cls):
        unpublished_articles = ArticleModel.find_all(published=False)
        return article_schema_many.dump(unpublished_articles), 200


# TODO zwracać tylko obublikowane artykuły, dodac nowy resource dla nieopubliskowanych
class Article(Resource):

    @classmethod
    def get(cls, slug: str):
        article = ArticleModel.find_by_slug(slug)
        if not article:
            return {"message": "Article not found"}, 404
        return article_schema.dump(article), 200

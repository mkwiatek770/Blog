import traceback

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_current_user
from flask_uploads import UploadNotAllowed

from libs import image_helper
from models import ArticleModel, TagModel, UserModel
from schemas.article import ArticleSchema
from schemas.image import ImageSchema

article_schema = ArticleSchema()
article_schema_many = ArticleSchema(many=True)
image_schema = ImageSchema()


class Articles(Resource):

    @classmethod
    def get(cls):
        published_articles = ArticleModel.find_all()
        return article_schema_many.dump(published_articles), 200

    @classmethod
    @jwt_required
    def post(cls):
        article_json = request.get_json()
        article_data = article_schema.load(article_json)

        if ArticleModel.find_by_title(article_data.title):
            return {"message": "Article with given title already exists"}

        article_data.save_to_db()
        return article_schema.dump(article_data), 201


class ArticleDetail(Resource):

    @classmethod
    def get(cls, slug: str):
        article = ArticleModel.find_by_slug(slug)
        if not article or not article.published_date:
            return {"message": "Article not found"}, 404
        return article_schema.dump(article), 200

    @classmethod
    @jwt_required
    def put(cls, slug: str):
        article = ArticleModel.find_by_slug(slug)
        if not article:
            return {"message": "Article not found"}, 404

        article_json = request.get_json()
        article.description = article_json["description"]
        article.content = article_json["content"]
        article.save_to_db()

        return article_schema.dump(article), 204

    @classmethod
    @jwt_required
    def delete(cls, slug: str):
        article = ArticleModel.find_by_slug(slug)
        if not article:
            return {"message": "Article not found"}, 404
        article.delete_from_db()
        return {"message": "Article deleted"}, 200


class DraftArticles(Resource):

    @classmethod
    @jwt_required
    def get(cls):
        unpublished_articles = ArticleModel.find_all(published=False)
        return article_schema_many.dump(unpublished_articles), 200


class DraftArticleDetail(Resource):

    @classmethod
    @jwt_required
    def get(cls, slug: str):
        article = ArticleModel.find_by_slug(slug)
        if not article:
            return {"message": "Article does not exist"}, 404
        if article.published_date:
            return {"message": "Article already published, it's not in draft list"}, 400
        return article_schema.dump(article), 200


class ArticleSetTags(Resource):

    @classmethod
    @jwt_required
    def put(cls, slug):

        article = ArticleModel.find_by_slug(slug)
        if not article:
            return {"message": "Article does not exist"}, 404
        tags = request.get_json()["tags"]
        article.tags = []
        for tag in tags:
            tag_object = TagModel.get_or_create(name=tag)
            if not tag_object in article.tags:
                article.tags.append(tag_object)
        article.save_to_db()

        return article_schema.dump(article), 200


class ArticleUploadImage(Resource):

    @classmethod
    @jwt_required
    def put(cls, slug):
        article = ArticleModel.find_by_slug(slug)
        if not article:
            return {"message": "Article does not exist"}, 404

        data = image_schema.load(request.files)
        folder = "article_images"

        try:
            image_path = image_helper.save_image(data["image"], folder=folder)
            basename = image_helper.get_basename(image_path)

            previous_article_image = article.image_url
            article.image_url = basename
            article.save_to_db()

            if previous_article_image:
                image_helper.delete_image(previous_article_image, folder)

            return {"message": "Image {} uploaded".format(basename)}, 201
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": "Extension not allowed"}, 400
        except Exception:
            traceback.print_exc()
            return {"message": "Internal server error"}, 500


class ArticlePublish(Resource):

    @classmethod
    @jwt_required
    def post(cls, slug):
        article = ArticleModel.find_by_slug(slug)
        if not article:
            return {"message": "Article not found"}, 404
        if not article.image_url:
            return {"message": "Article must contain image before publishing"}, 400
        if article.tags == []:
            return {"message": "Article must have at least one tag assigned"}, 400

        article.publish()
        return {"message": "Article has been published"}, 200


class ArticleUnpublish(Resource):

    @classmethod
    @jwt_required
    def post(cls, slug):
        article = ArticleModel.find_by_slug(slug)
        if not article:
            return {"message": "Article not found"}, 404
        article.unpublish()
        return {"message": "Article has been unpublished"}, 200


class ArticleLike(Resource):

    @classmethod
    @jwt_required
    def post(cls, slug):
        article = ArticleModel.find_by_slug(slug)
        if not article:
            return {"message": "Article not found"}, 404
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        if user == article.author:
            return {"message": "You can't like your own article"}, 403
        if user in article.likes:
            return {"message": "You can't like this article twice"}, 403

        article.likes.append(user)
        article.save_to_db()
        return {"message": "Article with id={} has been liked by {}".format(article.id, user.username)}, 200


class ArticleRevokeLike(Resource):

    @classmethod
    @jwt_required
    def post(cls, slug):
        article = ArticleModel.find_by_slug(slug)
        if not article:
            return {"message": "Article not found"}, 404
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        if not user in article.likes:
            return {"message": "You have to like this article before you can revoke like"}, 403

        article.likes.remove(user)
        article.save_to_db()
        return {"message": "Article with id={} has been disliked by {}".format(article.id, user.username)}, 200


class ArticleChangeTitle(Resource):

    @classmethod
    @jwt_required
    def post(cls, slug):
        new_title = request.get_json()["title"]
        article = ArticleModel.find_by_slug(slug)
        if not article:
            return {"message": "Article not found"}, 404
        if new_title == article.title:
            return {"message": "You're trying to change to existing title"}
        if ArticleModel.find_by_title(new_title):
            return {"message": "This title is taken"}

        article.title = new_title
        article.save_to_db()
        return {"message": "Title has been changed"}, 200

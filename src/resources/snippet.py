from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from models import SnippetModel, TagModel
from schemas.snippet import SnippetSchema


snippet_schema = SnippetSchema()
snippet_schema_many = SnippetSchema(many=True)


class Snippets(Resource):

    @classmethod
    def get(cls):
        snippets = SnippetModel.find_all()
        return snippet_schema_many.dump(snippets)

    @classmethod
    def post(cls):
        snippet_json = request.get_json()
        snippet = snippet_schema.load(snippet_json)
        if SnippetModel.find_by_title(snippet.title):
            return {"message": "This title is already taken"}, 400

        tags = snippet.tags
        snippet.tags = []
        for tag in tags:
            tag_object = TagModel.get_or_create(tag.name)
            snippet.tags.append(tag_object)
        snippet.save_to_db()
        return snippet_schema.dump(snippet), 201


class SnippetDetail(Resource):

    @classmethod
    def get(cls, slug: str):
        snippet = SnippetModel.find_by_slug(slug)
        if not snippet or snippet.published_date == None:
            return {"message": "Snippet does not exist"}, 404
        return snippet_schema.dump(snippet), 200

    @classmethod
    @jwt_required
    def put(cls, slug: str):
        snippet_json = request.get_json()
        snippet = SnippetModel.find_by_slug(slug)
        if not snippet:
            return {"message": "Snippet does not exist"}, 404

        snippet.description = snippet_json["description"]
        snippet.code = snippet_json["code"]
        snippet.language = snippet_json["language"]
        snippet.tags = []
        tags = snippet_json.get("tags")
        if tags:
            for tag in tags:
                tag_object = TagModel.get_or_create(tag["name"])
                snippet.tags.append(tag_object)
        snippet.save_to_db()
        return snippet_schema.dump(snippet), 200

    @classmethod
    @jwt_required
    def delete(cls, slug: str):
        snippet = SnippetModel.find_by_slug(slug)
        if not snippet:
            return {"message": "Snippet does not exist"}, 404
        snippet.delete_from_db()
        return {"message": "Snippet deleted"}, 200


class SnippetsNotApproved(Resource):

    @classmethod
    @jwt_required
    def get(cls):
        snippets = SnippetModel.find_all(published=False)
        return snippet_schema_many.dump(snippets), 200


class SnippetNotAppprovedDetail(Resource):

    @classmethod
    def get(cls, slug: str):
        snippet = SnippetModel.find_by_slug(slug)
        if not snippet or snippet.published_date:
            return {"message": "Snippet does not exist"}, 404
        return snippet_schema.dump(snippet)


class ApproveSnippet(Resource):

    @classmethod
    @jwt_required
    def post(cls, slug: str):
        snippet = SnippetModel.find_by_slug(slug)
        if not snippet:
            return {"message": "Snippet not found"}, 404
        if snippet.published_date:
            return {"message": "Snippet have been already approved"}, 400
        snippet.approve()
        return {"message": "Snippet has been published"}, 200


class RevokeApprovalSnippet(Resource):

    @classmethod
    @jwt_required
    def post(cls, slug: str):
        snippet = SnippetModel.find_by_slug(slug)
        if not snippet:
            return {"message": "Snippet not found"}, 404
        if not snippet.published_date:
            return {"message": "Snippet is not published yet"}, 400
        snippet.revoke_approval()
        return {"message": "Snippet's approval has been revoked"}, 200

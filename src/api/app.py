from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_uploads import configure_uploads, patch_request_class
from marshmallow import ValidationError
from dotenv import load_dotenv

load_dotenv('./.env', verbose=True)

from libs.image_helper import IMAGE_SET
from resources.user import UserLogin, UserLogout, TokenRefresh, User, UserAvatar
from resources.article import (
    Articles,
    ArticleDetail,
    DraftArticles,
    DraftArticleDetail,
    ArticleSetTags,
    ArticleUploadImage,
    ArticlePublish,
    ArticleUnpublish,
    ArticleLike,
    ArticleRevokeLike,
    ArticleChangeTitle
)
from resources.snippet import (
    Snippets,
    SnippetsNotApproved,
    SnippetDetail,
    SnippetNotAppprovedDetail,
    ApproveSnippet,
    RevokeApprovalSnippet
)
from settings.blacklist import BLACKLIST
from settings.ma import ma
from settings.db import db


app = Flask(__name__)
app.config.from_pyfile("./settings/default_config.py")
app.config.from_envvar("APPLICATION_SETTINGS")
# set max size of image to 10MB
patch_request_class(app, size=10 * 1024 * 1024)
configure_uploads(app, IMAGE_SET)
api = Api(app)
jwt = JWTManager(app)
migrate = Migrate(app=app, db=db)
bcrypt = Bcrypt(app)
CORS(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.shell_context_processor
def make_shell_context():
    db.init_app(app)
    return {'db': db}

# global error handler
@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

# This method will check if a token is blacklisted, and will be called automatic
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST

# User endpoints
api.add_resource(UserLogin, "/api/v1/login")
api.add_resource(UserLogout, "/api/v1/logout")
api.add_resource(TokenRefresh, "/api/v1/refresh")
api.add_resource(User, "/api/v1/users/<string:username>")
api.add_resource(UserAvatar, "/api/v1/users/<string:username>/avatar")
# Article endpoints
api.add_resource(Articles, "/api/v1/articles")
api.add_resource(ArticleDetail, "/api/v1/articles/<string:slug>")
api.add_resource(DraftArticles, "/api/v1/articles/draft")
api.add_resource(DraftArticleDetail, "/api/v1/articles/draft/<string:slug>")
api.add_resource(ArticleSetTags, "/api/v1/articles/<string:slug>/tags")
api.add_resource(ArticleUploadImage, "/api/v1/articles/<string:slug>/image")
api.add_resource(ArticlePublish, "/api/v1/articles/<string:slug>/publish")
api.add_resource(ArticleUnpublish, "/api/v1/articles/<string:slug>/unpublish")
api.add_resource(ArticleLike, "/api/v1/articles/<string:slug>/like")
api.add_resource(ArticleRevokeLike, "/api/v1/articles/<string:slug>/revoke-like")
api.add_resource(ArticleChangeTitle, "/api/v1/articles/<string:slug>/new-title")
# Snippets endpoint
api.add_resource(Snippets, "/api/v1/snippets")
api.add_resource(SnippetsNotApproved, "/api/v1/snippets-not-approved")
api.add_resource(SnippetDetail, "/api/v1/snippets/<string:slug>")
api.add_resource(SnippetNotAppprovedDetail, "/api/v1/snippets-not-approved/<string:slug>")
api.add_resource(ApproveSnippet, "/api/v1/snippets/<string:slug>/approve")
api.add_resource(RevokeApprovalSnippet, "/api/v1/snippets/<string:slug>/revoke")


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    app.run(port=5000)

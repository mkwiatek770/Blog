from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_uploads import configure_uploads, patch_request_class
from marshmallow import ValidationError
from dotenv import load_dotenv

load_dotenv('./.env', verbose=True)

from libs.image_helper import IMAGE_SET
from resources.user import UserLogin, UserLogout, TokenRefresh, User, UserAvatar
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


@app.before_first_request
def create_tables():
    db.create_all()

# global error handler
@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

# This method will check if a token is blacklisted, and will be called automatic
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(UserLogin, "/api/v1/login")
api.add_resource(UserLogout, "/api/v1/logout")
api.add_resource(TokenRefresh, "/api/v1/refresh")
api.add_resource(User, "/api/v1/users/<string:username>")
api.add_resource(UserAvatar, "/api/v1/users/<string:username>/avatar")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    app.run(port=5000)

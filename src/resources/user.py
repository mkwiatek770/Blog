import traceback
import os
from flask import request, send_file
from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask_jwt_extended import (
    jwt_refresh_token_required,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    get_raw_jwt,
    jwt_required
)

from libs import image_helper
from settings.blacklist import BLACKLIST
from schemas.user import UserSchema
from models import UserModel
from schemas.image import ImageSchema

user_schema = UserSchema()
image_schema = ImageSchema()


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)
        user = UserModel.find_by_username(user_data.username)

        if user and user.check_password(user_json["password"]):

            if user.active:
                access_token = create_access_token(
                    identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}, 200
            return {"message": "User {} is not active".format(user.username)}, 400
        return {"message": "Invalid username or password"}, 401


class UserLogout(Resource):

    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": "User successfully logged out"}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


class User(Resource):
    """
    Resource to access user data.
    Specific user will be identified by username
    """
    @classmethod
    def get(cls, username: str):
        user = UserModel.find_by_username(username)
        if not user:
            return {"message": "User {} not found".format(username)}, 404
        return user_schema.dump(user), 200


class UserAvatar(Resource):
    """
    Resource to handle specific user avatar.
    """

    @classmethod
    def get(cls, username: str):
        user = UserModel.find_by_username(username)
        if not user:
            return {"message": "User {} not found".format(username)}, 404
        if user.avatar_name == "":
            return {"message": "Avatar for user {} not found".format(username)}, 404
        folder = "avatars"
        path = image_helper.get_path(user.avatar_name, folder)
        print(path)
        try:
            return send_file(path)
        except FileNotFoundError:
            return {"message": "Image not found"}, 404

    @classmethod
    @jwt_required
    def put(cls, username: str):
        user_id = get_jwt_identity()
        user = UserModel.find_by_username(username)
        if not user:
            return {"message": "User {} not found".format(username)}, 404
        if not user.id == user_id:
            return {"message": "You can't manipulate other user's avatars."}, 403

        data = image_schema.load(request.files)
        folder = "avatars"
        try:
            image_path = image_helper.save_image(data["image"], folder=folder)
            basename = image_helper.get_basename(image_path)

            previous_avatar_name = user.avatar_name
            user.avatar_name = basename
            user.save_to_db()

            if previous_avatar_name != "":
                image_helper.delete_image(previous_avatar_name, folder)

            return {"message": "Image {} uploaded".format(basename)}, 201
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": "Extension not allowed"}, 400
        except Exception:
            traceback.print_exc()
            return {"message": "Internal server error"}, 500

    @classmethod
    @jwt_required
    def delete(cls, username: str):
        user_id = get_jwt_identity()
        user = UserModel.find_by_username(username)
        if not user:
            return {"message": "User {} not found".format(username)}, 404
        if not user.id == user_id:
            return {"message": "You can't manipulate other user's avatars."}, 403
        if user.avatar_name == "":
            return {"message": "You don't have avatar"}, 400

        folder = "avatars"
        avatar_name = user.avatar_name
        try:
            path = image_helper.get_path(avatar_name, folder)
            user.avatar_name = ""
            user.save_to_db()
            os.remove(path)
            return {"message": "Avatar has been removed"}, 200
        except FileNotFoundError:
            return {"message": "Avatar not found in database"}, 400
        except Exception:
            traceback.print_exc()
            return {"message": "Internal server error"}, 500

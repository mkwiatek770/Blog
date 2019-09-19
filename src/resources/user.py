from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_refresh_token_required,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    get_raw_jwt,
    jwt_required
)

from settings.blacklist import BLACKLIST
from schemas.user import UserSchema
from models.user import UserModel

user_schema = UserSchema()


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

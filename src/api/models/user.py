import bcrypt
from datetime import datetime
from typing import List
from settings.db import db


class UserModel(db.Model):
    __tablename__ = "blog_user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(180), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    created_date = db.Column(db.DateTime, default=datetime.now)
    active = db.Column(db.Boolean, default=False)
    is_staff = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)
    # path to image file
    avatar_name = db.Column(db.String)

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    def set_password(self, password: str) -> None:
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

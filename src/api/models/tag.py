from typing import Union
from settings.db import db


class TagModel(db.Model):
    __tablename__ = "blog_tag"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    @classmethod
    def find_by_id(cls, _id: int) -> Union["TagModel", None]:
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name: str) -> Union["TagModel", None]:
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_or_create(cls, name: str) -> "TagModel":
        tag = cls.find_by_name(name)
        if not tag:
            tag = cls(name=name)
            tag.save_to_db()
        return tag

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

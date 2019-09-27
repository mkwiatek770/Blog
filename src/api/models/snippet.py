from datetime import datetime
from typing import List, Union
from settings.db import db


snippet_tags = db.Table('blog_snippet_tag',
                        db.Column('tag_id', db.Integer,
                                  db.ForeignKey('blog_tag.id')),
                        db.Column('snippet_id', db.Integer,
                                  db.ForeignKey('blog_snippet.id'))
                        )


class SnippetModel(db.Model):
    __tablename__ = "blog_snippet"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=False)
    language = db.Column(db.String, nullable=False)
    # kiedyś zrobić ForeignKey do blog_user
    author = db.Column(db.String, nullable=False)

    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    published_date = db.Column(db.DateTime)

    # likes = db.relationship("UserModel", secondary=snippet_likes)   <-- dodać jak już będzie opcja logowania się
    tags = db.relationship("TagModel", secondary=snippet_tags)

    @classmethod
    def find_by_id(cls, _id: int) -> Union["SnippetModel", None]:
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls, published: bool = True) -> List["SnippetModel"]:
        if published:
            return cls.query.filter(cls.published_date != None)
        return cls.query.filter(cls.published_date == None)

    @classmethod
    def find_by_slug(cls, slug: str) -> Union["SnippetModel", None]:
        unslugged_title = " ".join(slug.split("-"))
        return cls.query.filter(cls.title.ilike(unslugged_title)).first()

    @classmethod
    def find_by_title(cls, title: str) -> Union["SnippetModel", None]:
        return cls.query.filter_by(title=title).first()

    def approve(self) -> None:
        self.published_date = datetime.utcnow()
        self.save_to_db()

    def revoke_approval(self) -> None:
        self.published_date = None
        self.save_to_db()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

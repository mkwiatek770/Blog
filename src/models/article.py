from datetime import datetime
from typing import List
from slugify import slugify
from settings.db import db


article_likes = db.Table('likes_in_article',
                         db.Column('user_id', db.Integer,
                                   db.ForeignKey('blog_user.id')),
                         db.Column('article_id', db.Integer,
                                   db.ForeignKey('blog_article.id'))
                         )

article_tags = db.Table('blog_article_tag',
                        db.Column('tag_id', db.Integer,
                                  db.ForeignKey('blog_tag.id')),
                        db.Column('article_id', db.Integer,
                                  db.ForeignKey('blog_article.id'))
                        )


class ArticleModel(db.Model):
    __tablename__ = "blog_article"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("blog_user.id"))
    title = db.Column(db.String(200), nullable=False, unique=True)
    content = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    published_date = db.Column(db.DateTime)
    image_url = db.Column(db.String)

    author = db.relationship("UserModel")
    likes = db.relationship("UserModel", secondary=article_likes)
    tags = db.relationship("TagModel", secondary=article_tags)

    @property
    def slug(self) -> str:
        return slugify(self.title)

    @classmethod
    def find_by_id(cls, _id: int) -> "ArticleModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls, published: bool = True) -> List["ArticleModel"]:
        if published:
            return cls.query.filter(cls.published_date != None)
        return cls.query.filter(cls.published_date == None)

    @classmethod
    def find_by_slug(cls, slug: str) -> "ArticleModel":
        unslugged_title = " ".join(slug.split("-"))
        return cls.query.filter(cls.title.ilike(unslugged_title)).first()

    @classmethod
    def find_by_title(cls, title: str) -> "ArticleModel":
        return cls.query.filter_by(title=title).first()

    def publish(self) -> None:
        self.published_date = datetime.utcnow()
        self.save_to_db()

    def unpublish(self) -> None:
        self.published_date = None
        self.save_to_db()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

from datetime import datetime
from settings.db import db


class ArticleLikes(db.Model):
    __tablename__ = "blog_article_likes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("blog_user.id"))
    article_id = db.Column(db.Integer, db.ForeignKey("blog_article.id"))


class ArticleTags(db.Model):
    __tablename__ = "blog_article_tags"
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("blog_tag.id"))
    article_id = db.Column(db.Integer, db.ForeignKey("blog_article.id"))


class Article(db.Model):
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
    likes = db.relationship("ArticleLikes")
    tags = db.relationship("ArticleTags")

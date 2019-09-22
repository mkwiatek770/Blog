from datetime import datetime
from slugify import slugify
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
    likes = db.relationship("ArticleLikes")
    tags = db.relationship("ArticleTags")

    @property
    def slug(self) -> str:
        return slugify(self.title)

    @classmethod
    def find_by_id(cls, _id: int) -> "ArticleModel":
        return cls.query.filter_by(id=_id).first()

    def publish(self) -> None:
        self.published_date = datetime.utcnow()
        self.save_to_db()

    def unplish(self) -> None:
        self.published_date = None
        self.save_to_db()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
SECRET_KEY = os.environ["APP_SECRET_KEY"]
JWT_BLACKLIST_ENABLED = True
UPLOADED_IMAGES_DEST = os.path.join("static", "images")
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

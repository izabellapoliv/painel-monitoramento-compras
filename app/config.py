import os

SQLALCHEMY_DATABASE_URI = f'mysql://{os.environ.get("DATABASE_USERNAME")}:{os.environ.get("DATABASE_PASSWORD")}@{os.environ.get("DATABASE_HOST")}/{os.environ.get("DATABASE_NAME")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

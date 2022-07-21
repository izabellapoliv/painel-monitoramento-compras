from flask import current_app

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(current_app)
ma = Marshmallow(current_app)

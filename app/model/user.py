import datetime

from app import db, ma

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, login, password) -> None:
        self.login = login
        self.password = password

class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'login', 'password')


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

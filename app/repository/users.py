from werkzeug.security import generate_password_hash
from flask import request, jsonify

from app.lib.extensions import db
from app.model.user import Users, user_schema, users_schema

def create():
    login = request.json['login']
    password = request.json['password']
    password_hashed = generate_password_hash(password)

    user = Users(login, password_hashed)
    try:
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify(result), 201
    except Exception as inst:
        return jsonify({'message': inst.args}), 500

def get_by_login(login) -> Users:
    try:
        return Users.query.filter(Users.login == login).one()
    except:
        return None

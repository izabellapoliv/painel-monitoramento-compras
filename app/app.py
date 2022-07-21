# coding: utf-8

import os
from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from lib.security import validate_token
from exceptions.auth_error import AuthError

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)

from repository import users
from repository import transactions


@app.before_request
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    # validate_token(auth)


@app.route("/")
def welcome():
    return render_template("index.html")


@app.route('/api/usuarios', methods=['POST'])
def post_user():
    return users.create()


@app.route('/api/estoque', methods=['POST'])
def change_inventory():
    return transactions.create()


@app.route("/api/estoque", methods=["GET"])
def get_inventory():
    return transactions.search()


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


if __name__ == "__main__":
    app.run(
        debug=True if os.environ.get("FLASK_ENV") == "development" else False,
        host="0.0.0.0",
    )

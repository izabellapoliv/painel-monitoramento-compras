# coding: utf-8

import os
from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin

from app.lib.extensions import db, ma

from app.lib.security import auth
from app.exceptions.auth_error import AuthError

from app.repository import users
from app.repository import transactions

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    register_extensions(app)


    @app.before_request
    def get_token_auth_header():
        auth = request.headers.get('Authorization', None)
        # validate_token(auth)


    @app.route("/")
    def welcome():
        return render_template("index.html")


    @app.route("/api/auth", methods=['POST'])
    def authenticate():
        return auth()


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


    # if __name__ == "__main__":
    #     app.run(
    #         debug=os.environ.get("FLASK_ENV") == "development",
    #         host='0.0.0.0',
    #     )

    return app

def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)

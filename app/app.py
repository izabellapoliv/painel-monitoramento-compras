# coding: utf-8

import os
from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin

# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.exc import IntegrityError

from model.credit import Credit, CreditSchema
from model.debit import Debit, DebitSchema
from model.transaction import TransactionSchema
from model.transaction_type import TransactionType

from lib.security import validate_token
from exceptions.auth_error import AuthError

app = Flask(__name__)
app.config.from_object('config')
# SQLALCHEMY_DATABASE_URI = f'mysql://{os.environ.get("DATABASE_USERNAME")}:{os.environ.get("DATABASE_PASSWORD")}@{os.environ.get("DATABASE_HOST")}/{os.environ.get("DATABASE_NAME")}'
# app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
# db = SQLAlchemy(app)


transactions = [
  Credit(1, 50),
  Credit(2, 40),
  Debit(3, 3),
  Debit(4, 2)
]


@app.before_request
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    validate_token(auth)


@app.route("/")
def welcome():
    return render_template("index.html")


@app.route("/api/estoque", methods=["GET"])
def get_inventory():
    schema = TransactionSchema(many=True)
    return jsonify(schema.dump(transactions))


@app.route('/api/estoque', methods=['POST'])
def change_inventory():
    schema = CreditSchema() if request.json["type"] == TransactionType.CREDIT else DebitSchema()
    transaction = schema.load({
        'id': transactions[-1].id + 1,
        'amount': request.json["amount"]
    })
    transactions.append(schema.dump(transaction))
    return schema.dump(transaction), 201


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

# coding: utf-8

from distutils.log import debug
import os
from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from model.credit import Credit, CreditSchema
from model.debit import Debit, DebitSchema
from model.transaction import TransactionSchema
from model.transaction_type import TransactionType

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = f'mysql://{os.environ.get("DATABASE_USERNAME")}:{os.environ.get("DATABASE_PASSWORD")}@{os.environ.get("DATABASE_HOST")}/{os.environ.get("DATABASE_NAME")}'
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)


transactions = [
  Credit(1, 50),
  Credit(2, 40),
  Debit(3, 3),
  Debit(4, 2)
]


@app.before_request
def limit_remote_addr():
    if app.debug == False:
        print('Validate client IP for example')


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


if __name__ == "__main__":
    app.run(
        debug=True if os.environ.get("FLASK_ENV") == "development" else False,
        host="0.0.0.0",
    )

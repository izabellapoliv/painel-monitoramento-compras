from app import app
from flask import Flask, render_template, request, jsonify

from model.credit import Credit, CreditSchema
from model.debit import Debit, DebitSchema
from model.transaction import TransactionSchema
from model.transaction_type import TransactionType


transactions = [
  Credit(1, 50),
  Credit(2, 40),
  Debit(3, 3),
  Debit(4, 2)
]


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

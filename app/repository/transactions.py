from flask import request, jsonify

from app import db
from model.credit_transaction import Credit
from model.debit_transaction import Debit
from model.transactions import Transactions, transactions_schema
from model.transaction_type import TransactionType

def create():
    type_t = request.json['type']
    amount = request.json['amount']

    transaction = Credit(amount) if type_t == TransactionType.CREDIT.value else Debit(amount)
    schema = transaction.get_schema()

    try:
        db.session.add(transaction)
        db.session.commit()
        result = schema.dump(transaction)
        return jsonify(result), 201
    except Exception as inst:
        return jsonify({'message': inst.args}), 500

def search():
    query = Transactions.query.filter().order_by('created_at').all()
    result = transactions_schema.dump(query)
    return jsonify(result)

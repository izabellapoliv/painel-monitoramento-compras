from flask import request, jsonify

from app.lib.extensions import db
from app.model.credit_transaction import Credit
from app.model.debit_transaction import Debit
from app.model.transactions import Transactions, transactions_schema
from app.model.transaction_type import TransactionType

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
    try:
        query = Transactions.query \
                            .filter() \
                            .order_by(Transactions.created_at.desc()) \
                            .order_by(Transactions.id.desc()) \
                            .all()
        result = transactions_schema.dump(query)
        return jsonify(result)
    except Exception as inst:
        return jsonify({'message': inst.args}), 500

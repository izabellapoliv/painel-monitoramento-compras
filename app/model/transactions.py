import datetime
from abc import ABC

from app import db, ma


class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Numeric, nullable=False)
    type = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, amount, type) -> None:
        self.amount = amount
        self.type = type


class TransactionsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'amount', 'type', 'description')


transaction_schema = TransactionsSchema()
transactions_schema = TransactionsSchema(many=True)

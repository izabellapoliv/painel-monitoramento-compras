from marshmallow import post_load

from .transaction import Transaction, TransactionSchema
from .transaction_type import TransactionType


class Credit(Transaction):
  def __init__(self, id, amount):
    super(Credit, self).__init__(id, amount, TransactionType.CREDIT)

  def __repr__(self):
    return '<Credit(name={self.id!r})>'.format(self=self)


class CreditSchema(TransactionSchema):
  @post_load
  def make(self, data, **kwargs):
    return Credit(**data)

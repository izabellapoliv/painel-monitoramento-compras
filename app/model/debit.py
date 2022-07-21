from marshmallow import post_load

from .transaction import Transaction, TransactionSchema
from .transaction_type import TransactionType


class Debit(Transaction):
  def __init__(self, id, amount):
    super(Debit, self).__init__(id, -abs(amount), TransactionType.DEBIT)

  def __repr__(self):
    return '<Debit(name={self.id!r})>'.format(self=self)


class DebitSchema(TransactionSchema):
  @post_load
  def make(self, data, **kwargs):
    return Debit(**data)

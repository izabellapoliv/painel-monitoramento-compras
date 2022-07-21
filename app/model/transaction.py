import datetime as dt

from abc import ABC, abstractmethod
from marshmallow import Schema, fields


class Transaction(ABC):
  def __init__(self, id, amount, type):
    self.id = id
    self.amount = amount
    self.type = type
    self.created_at = dt.datetime.now()

  def __repr__(self):
    return '<Transaction(name={self.id!r})>'.format(self=self)


class TransactionSchema(Schema):
  id = fields.Number()
  amount = fields.Number()
  type = fields.Str()
  created_at = fields.Date()

  @abstractmethod
  def make(self, data):
    pass

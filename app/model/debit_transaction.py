from .transactions import Transactions, TransactionsSchema
from .transaction_type import TransactionType

class Debit(Transactions):
  def __init__(self, amount) -> None:
    super(Debit, self).__init__(-abs(amount), TransactionType.DEBIT.value)

  def get_schema(many=False):
    return debit_schema if many else debits_schema


class DebitSchema(TransactionsSchema):
  pass


debit_schema = DebitSchema()
debits_schema = DebitSchema(many=True)

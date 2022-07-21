from .transactions import Transactions, TransactionsSchema
from .transaction_type import TransactionType

class Credit(Transactions):
  def __init__(self, amount) -> None:
    super(Credit, self).__init__(amount, TransactionType.CREDIT)

  def get_schema(many=False):
    return credit_schema if many else credits_schema


class CreditSchema(TransactionsSchema):
  pass


credit_schema = CreditSchema()
credits_schema = CreditSchema(many=True)

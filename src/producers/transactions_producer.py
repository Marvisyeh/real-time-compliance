from datetime import datetime
from pydantic import BaseModel
import random

class TransactionSchema(BaseModel):
  timestamp: str
  transaction_id: str
  amount: int
  currency: str
  status: str
  user_id: int


def transaction_generator():
  currencies = ["TWD", "USD", "EUR", "JPY", "GBP"]
  statuses = ["SUCCESS", "FAILED", "PENDING", "CANCELLED"]
  
  tx_id = f"tx_{random.randint(1000, 9999)}"
  
  return TransactionSchema(
    timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4] + "Z",
    transaction_id=tx_id,
    amount=random.randint(100, 10000),
    currency=random.choice(currencies),
    status=random.choice(statuses),
    user_id=random.randint(100, 9999)
  )


if __name__ == "__main__":
  # Generate a single transaction
  transaction = transaction_generator()
  print(transaction.model_dump_json(indent=2))
  
  # Generate multiple transactions
  print("\nGenerating 5 transactions:")
  for _ in range(5):
    transaction = transaction_generator()
    print(transaction.model_dump_json())
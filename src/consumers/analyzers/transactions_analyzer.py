from collections import defaultdict, deque
from datetime import datetime, timedelta

class TransactionsAnalyzer:
  def __init__(self):
    self.user_windows = defaultdict(deque)

  def process(self, data):
    user_id = data.get("user_id")
    amount = data.get("amount")
    service = "transaction-service"
    timestamp = data.get("timestamp")
    
    if amount > 10000:
      return self._alert(
        is_alert=True,
        alert_type="HIGH_AMOUNT",
        alert_level="CRITICAL",
        alert_title="High Transaction Amount",
        alert_message=f"user {user_id} amount={amount}",
        service=service,
        tags={"user_id": user_id},
        metrics={"amount": amount},
        timestamp=timestamp
      )

    if self._detect_high_frequency(user_id, timestamp):
      return self._alert(
        is_alert=True,
        alert_type="HIGH_FREQUENCY",
        alert_level="WARNING",
        alert_title="Frequent Transactions",
        alert_message=f"user {user_id} has too many transactions",
        service=service,
        tags={"user_id": user_id},
        metrics={},
        timestamp=timestamp
      )

    return self._no_alert(data)

  def _detect_high_frequency(self, user_id, timestamp):
    t = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    window = self.user_windows[user_id]

    window.append(t)
    cutoff = t - timedelta(seconds=300)

    while window and window[0] < cutoff:
        window.popleft()

    return len(window) >= 5
  
  def _alert(self, **kwargs):
    return {
      "is_alert": True,
      **kwargs
    }

  def _no_alert(self, data):
    return {
      "is_alert": False,
      "raw_data": data
    }
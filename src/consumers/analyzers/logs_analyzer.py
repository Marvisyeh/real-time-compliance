from datetime import datetime, timedelta
from collections import defaultdict, deque

class LogsAnalyzer:
  def __init__(self):
    self.users_windows = defaultdict(deque)
    self.error_windows = defaultdict(deque)

  def process(self, data):
    service = data.get("service")
    user_id = data.get("user_id")
    level = data.get("level")
    timestamp = data.get("timestamp")
    message = data.get("message", "")

    if level == "ERROR":
      # alert when error > 20 in five minutes in same service
      if self._detect_error_spike(service, timestamp):
        return self._alert(
          alert_type="ERROR_SPIKE",
          alert_level="CRITICAL",
          alert_title="Service Error Spike",
          alert_message=f"{service} has too many error logs.",
          service=service,
          tags={"level": "ERROR"},
          metrics={},
          timestamp=timestamp
        )
      
      # Particular word alert: failed
      if "failed" in message.lower():
        return self._alert(
          alert_type="LOG_KEYWORD",
          alert_level="WARNING",
          alert_title="Log Keyword Detected",
          alert_message=f"{service} log contains 'failed'",
          service=service,
          tags={"message": message},
          metrics={},
          timestamp=timestamp
        )
    
    else:
      # Same user error cluster
      if self._detect_user_spike(user_id, timestamp):
        return self._alert(
          alert_type="USER_ISSUE",
          alert_level="WARNING",
          alert_title="User Error Detected",
          alert_message=f"{user_id} too much error",
          user_id=user_id,
          tags={"message": message},
          metrics={},
          timestamp=timestamp
        )

    return self._no_alert(data)

  def _detect_error_spike(self, service, ts):
    t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    window = self.error_windows[service]

    window.append(t)
    cutoff = t - timedelta(seconds=180)

    while window and window[0] < cutoff:
      window.popleft()

    return len(window) >= 20

  def _detect_user_spike(self, user_id, ts):
    t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    window = self.users_windows[user_id]

    window.append(t)
    cutoff = t - timedelta(seconds=180)

    while window and window[0] < cutoff:
      window.popleft()

    return len(window) >= 10

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

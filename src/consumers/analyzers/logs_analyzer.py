from datetime import datetime, timedelta
from collections import defaultdict, deque

class LogsAnalyzer:
  def __init__(self):
    self.error_windows = defaultdict(deque)

  def process(self, data):
    service = data.get("service")
    level = data.get("level")
    timestamp = data.get("timestamp")
    message = data.get("message", "")

    if level == "ERROR":
      if self._detect_error_spike(service, timestamp):
        return self._alert(
          alert_type="ERROR_SPIKE",
          alert_level="CRITICAL",
          alert_title="Service Error Spike",
          alert_message=f"{service} has too many error logs.",
          service=service,
          tags={"level": "ERROR"},
          metrics={}
        )

      if "failed" in message.lower():
        return self._alert(
          alert_type="LOG_KEYWORD",
          alert_level="WARNING",
          alert_title="Log Keyword Detected",
          alert_message=f"{service} log contains 'failed'",
          service=service,
          tags={"message": message},
          metrics={}
        )

      return self._no_alert(data)


  def _detect_error_spike(self, service, ts):
    t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    window = self.error_windows[service]

    window.append(t)
    cutoff = t - timedelta(seconds=60)

    while window and window[0] < cutoff:
      window.popleft()

    return len(window) >= 20

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

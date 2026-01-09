from datetime import datetime, timedelta
from collections import defaultdict, deque

class MetricsAnalyzer:
  def __init__(self):
    self.metrics_windows = defaultdict(deque)

  def process(self, data):
    service = data.get("service")
    cpu = data.get("cpu", 0)
    latency_ms = data.get("latency_ms", 0)
    timestamp = data.get("timestamp")
    message = data.get("message", "")
    user_id = data.get("user_id", "")

    # cpu >= 80% and continue 5 mins
    if self._detect_high_cpu(service, timestamp):
      return self._alert(
        alert_type="HIGH_CPU",
        alert_level="WARNING",
        alert_title="High CPU",
        alert_message=f"{service} CPU {cpu}%",
        user_id=user_id,
        tags={"message": message},
        metrics={"cpu": cpu},
        timestamp=timestamp
      )
    
    # latency > 1000ms
    if latency_ms > 1000:
      return self._alert(
        alert_type="HIGH_LATENCY",
        alert_level="CRITICAL",
        alert_title="Latency Spike",
        alert_message=f"{service} latency={latency_ms}ms",
        user_id=user_id,
        tags={"message": message},
        metrics={"latency": latency_ms},
        timestamp=timestamp
      )
    
    # cpu and latency both high
    if cpu > 80 and latency_ms > 1000:
      return self._alert(
        alert_type="HIGH_CPU_Latency",
        alert_level="WARNING",
        alert_title="High CPU & Latency",
        alert_message=f"{service} CPU {cpu}% & latency {latency_ms}ms",
        user_id=user_id,
        tags={"message": message},
        metrics={"cpu": cpu, "latency": latency_ms},
        timestamp=timestamp
      )
    
    return self._no_alert(data)
  
  def _detect_high_cpu(self, service, timestamp):
    t = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    window = self.metrics_windows[service]

    window.append(t)
    cutoff = t - timedelta(seconds=300)

    while window and window[0] < cutoff:
      window.popleft()

    return len(window) >= 30
  
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
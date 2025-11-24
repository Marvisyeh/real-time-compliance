class MetricsAnalyzer:
  def process(self, data):
    service = data.get("service")
    cpu = data.get("cpu", 0)
    latency = data.get("latency_ms", 0)

    if cpu > 90:
      return {
        "is_alert": True,
        "alert_type": "HIGH_CPU",
        "alert_level": "WARNING",
        "alert_title": "High CPU",
        "alert_message": f"{service} CPU {cpu}%",
        "service": service,
        "tags": {},
        "metrics": {"cpu": cpu}
      }

    if latency > 300:
      return {
        "is_alert": True,
        "alert_type": "HIGH_LATENCY",
        "alert_level": "CRITICAL",
        "alert_title": "Latency Spike",
        "alert_message": f"{service} latency={latency}ms",
        "service": service,
        "tags": {},
        "metrics": {"latency": latency}
      }

    return {"is_alert": False, "raw_data": data}

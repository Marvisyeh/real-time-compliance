import requests

from consumers.config.settings import AlertConfig


class AlertHandler:
  def send_alert(self, alert: dict):
    embed = {
      "title": alert.get("title", "Alert"),
      "description": alert.get("message", ""),
      "color": self._level_to_color(alert.get("level", "INFO")),
      "fields": []
    }

    embed["fields"].append({
      "name": "Alert Type",
      "value": alert.get("alert_type", "N/A"),
      "inline": True
    })

    embed["fields"].append({
      "name": "Service",
      "value": alert.get("service", "N/A"),
      "inline": True
    })

    embed["fields"].append({
      "name": "Level",
      "value": alert.get("level", "INFO"),
      "inline": True
    })

    tags = alert.get("tags", {})
    for key, val in tags.items():
      embed["fields"].append({
        "name": key,
        "value": str(val),
        "inline": False
      })
        
    metrics = alert.get("metrics", {})
    for key, val in metrics.items():
      embed["fields"].append({
        "name": key,
        "value": str(val),
        "inline": True
      })


    payload = {
      "username": "RealTimeApp Notify",
      "avatar_url": AlertConfig.AVATAR_URL,
      # "content": f"Service: {service}",
      "embeds": [embed]
    }

    try:
      response = requests.post(
        url = AlertConfig.DISCORD_WEBHOOK_URL,
        json=payload,
        timeout=3
      )
      response.raise_for_status()
    except Exception as e:
      print(f"[AlertHandler] Discord webhook failed: {e}")

  def _level_to_color(self, level: str):
    colors = {
      "INFO": 3447003,
      "WARNING": 15105570,
      "CRITICAL": 15158332   # red
    }
    return colors.get(level.upper(), 3447003)


if __name__ == "__main__":
  sample_alert = {
    "alert_id": "uuid-003",
    "alert_type": "HIGH_LATENCY",
    "title": "Latency Spike",
    "message": "payment latency reached 450ms",
    "level": "CRITICAL",
    "service": "payment-service",
    "tags": {"user_id": 88},
    "metrics": {"observed": 450, "threshold": 300},
    "created_at": "2025-11-22T10:20:30Z"
  }
  a = AlertHandler()
  a.send_alert(sample_alert)
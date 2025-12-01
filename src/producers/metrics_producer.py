from datetime import datetime
from pydantic import BaseModel
import random

class MetricsSchema(BaseModel):
  timestamp: str
  service: str
  cpu: float
  latency_ms: int


def metrics_generator():
  services = [
    "inventory-api",
    "payment-api",
    "user-api",
    "auth-service",
    "notification-service"
  ]
  
  return MetricsSchema(
    timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    service=random.choice(services),
    cpu=round(random.uniform(10.0, 99.9), 1),
    latency_ms=random.randint(50, 1000)
  )


if __name__ == "__main__":
  # Generate a single metric
  metric = metrics_generator()
  print(metric.model_dump_json(indent=2))
  
  # Generate multiple metrics
  print("\nGenerating 5 metrics:")
  for _ in range(5):
    metric = metrics_generator()
    print(metric.model_dump_json())
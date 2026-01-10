from datetime import datetime
from pydantic import BaseModel
import random


class LogsSchema(BaseModel):
    timestamp: str
    service: str
    level: str
    message: str
    user_id: int


def logs_generator():
    services = ["auth-service", "payment-service",
                "user-service", "api-gateway", "database-service"]
    levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
    messages = {
        "INFO": ["User logged in successfully", "Request processed", "Service started"],
        "WARNING": ["High memory usage detected", "Slow query detected", "Connection timeout"],
        "ERROR": ["User login failed", "Database connection lost", "Payment processing failed"],
        "DEBUG": ["Processing request", "Validating user input", "Cache hit"]
    }

    level = random.choice(levels)

    return LogsSchema(
        timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        service=random.choice(services),
        level=level,
        message=random.choice(messages[level]),
        user_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    log = logs_generator()
    print(log.model_dump_json(indent=2))

    print("\nGenerating 5 logs:")
    for _ in range(5):
        log = logs_generator()
        print(log.model_dump_json())

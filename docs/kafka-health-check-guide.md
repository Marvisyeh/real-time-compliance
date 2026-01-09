# Kafka Health Check Guide

When working with Kafka in Docker containers, it's important to verify that the service is not only running but also **fully functional**. This guide provides practical steps to check the health of your Kafka container.

---

## 1. ✅ Status Check

Verify if the container is running and its health status.

- **Command:**

  ```bash
  docker compose -f ./infra/docker/docker-compose.yml ps
  ```

- **What to Look For:**

  - The `State` column should show `Up`.
  - With a health check implemented (see Section 4), you may also see:

    - `Up (healthy)`
    - `Up (starting)`
    - `Up (unhealthy)` → Something is wrong.

---

## 2. 📝 Log Check

Inspect Kafka logs for success or error indicators.

- **Command:**

  ```bash
  docker compose -f ./infra/docker/docker-compose.yml logs broker
  ```

  _(Replace `broker` with your Kafka service name.)_

- **What to Look For:**

  - **Success (KRaft):**
    `[KafkaServer id=1] started (kafka.server.KafkaServer)`
  - **Success (ZooKeeper):**
    `[KafkaServer id=1] The broker is now registered in ZooKeeper as ID 1`
  - **Failure:** Any lines containing `ERROR`, `FATAL`, `Exception`

---

## 3. 🧪 Functionality Test

Verify Kafka is working by producing and consuming a message.

1. **Produce a Message:**

   ```bash
   docker compose exec broker /opt/kafka/bin/kafka-console-producer.sh \
     --bootstrap-server broker:9092 \
     --topic test-topic
   ```

   - Type a message (e.g., `Hello Kafka!`) and press Enter.
   - Press `Ctrl+C` to exit.

2. **Consume the Message:**

   ```bash
   docker compose exec broker /opt/kafka/bin/kafka-console-consumer.sh \
     --bootstrap-server broker:9092 \
     --topic test-topic \
     --from-beginning
   ```

   - If you see `Hello Kafka!`, your Kafka setup is functional.

---

## 4. 🛡️ Implement a Docker Health Check

Add a health check to your `broker` service in `docker-compose.yml`:

```yaml
services:
  broker:
    image: bitnami/kafka:latest
    # ... other configurations
    healthcheck:
      test:
        [
          "CMD",
          "kafka-cluster.sh",
          "cluster-id",
          "--bootstrap-server",
          "localhost:9092",
        ]
      interval: 10s
      timeout: 5s
      retries: 5
```

- **After this is added**, running `docker compose ps` will show:

  - `Up (healthy)` → Kafka is ready
  - `Up (starting)` → Kafka is initializing
  - `Up (unhealthy)` → Kafka is running but not ready

You can also make dependent services wait for Kafka to be ready:

```yaml
app_service:
  depends_on:
    broker:
      condition: service_healthy
```

---

## 5. 🛠 Troubleshooting Tips

- **Container stuck at `(starting)` or `(unhealthy)`?**

  - Check for port binding issues or volume conflicts
  - Ensure `broker.id` and cluster metadata are correct
  - Confirm KRaft or ZooKeeper configs are not mixed up

- **No logs or command not found errors?**

  - Ensure the correct image and internal paths (`/opt/kafka/...`) are used
  - Use `docker compose exec broker bash` to inspect the container manually

---

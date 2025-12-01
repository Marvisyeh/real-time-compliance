# 📡 Real-Time Compliance / Anomaly Monitoring

Current status: three Kafka producers (logs/metrics/transactions) are working, two consumers (S3 backup + rule-based anomaly detection) are running, Discord alerts fire, and anomaly events are written to PostgreSQL. FastAPI and the dashboard are not implemented yet. Docker Compose includes Kafka (KRaft), Postgres, and dev containers.

---

## Status at a Glance

- ✅ Producers: randomized logs / metrics / transactions sent to Kafka
- ✅ Consumers:
  - `BackupS3Consumer`: save raw JSON to S3 (assume-role required)
  - `AnalysisConsumer`: per-type rules, Discord alerts, insert into Postgres `anomaly_events`
- ✅ Docker Compose: Kafka (KRaft), Postgres, producer/consumer dev containers
- ⏳ Database: only anomaly insert logic; table creation/migrations are manual
- 🚧 FastAPI, Dashboard: folders exist, no implementation
- 🚧 Tests: basic function test stubs only

---

## Architecture (what runs today)

1. Python producers emit three event types -> Kafka topics `logs` / `metrics` / `transactions`
2. Consumer A: writes raw messages to S3 (`PREFIX/YYYYMMDD/<timestamp>.json`)
3. Consumer B: rule evaluation by type
   - Logs: ERROR spike in 3 minutes >= 20, message contains "failed", or per-user spike
   - Metrics: sustained CPU >= 80%, latency > 1000ms, or both high
   - Transactions: amount > 10000, or high-frequency per user within 5 minutes
   - Alerts -> Discord webhook; anomalies -> Postgres `anomaly_events`

---

## Project Structure

```
src/
  producers/        # event generators + Kafka producer
  consumers/        # S3 backup, anomaly analysis, alerts, DB writes
  dashboard/        # placeholder
  api/              # placeholder
infra/
  docker/           # Dockerfile, docker-compose.yml, requirements
docs/               # PRD, TODO, Kafka health check guide
db-data/            # Postgres volume (mounted by docker compose)
```

---

## Quickstart

### 1) Prepare `.env` (Kafka KRaft + service settings)
`infra/docker/docker-compose.yml` reads the following keys (fill them yourself):
- Kafka (KRaft): `KAFKA_NODE_ID`, `KAFKA_PROCESS_ROLES`, `KAFKA_LISTENERS`, `KAFKA_ADVERTISED_LISTENERS`, `KAFKA_CONTROLLER_LISTENER_NAMES`, `KAFKA_LISTENER_SECURITY_PROTOCOL_MAP`, `KAFKA_CONTROLLER_QUORUM_VOTERS`, `KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR`, `KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR`, `KAFKA_TRANSACTION_STATE_LOG_MIN_ISR`, `KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS`, `KAFKA_NUM_PARTITIONS`
- Pipeline: `KAFKA_SERVER_1`, `AWS_REGION`, `S3_BUCKET`, `PREFIX`, `ROLE_ARN`, `DISCORD_WEBHOOK_URL`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`

For local testing, point Kafka/DB to `localhost`; leave Discord/S3 empty to avoid real calls.

### 2) Start Kafka and Postgres
```bash
docker compose -f infra/docker/docker-compose.yml up -d broker db
```

### 3) Start the Producer
```bash
python - <<'PY'
from producers import DataProducer
p = DataProducer(bootstrap_servers="localhost:9092")
p.start_data_stream(duration_seconds=120, interval_seconds=1)
PY
```

### 4) Start the Consumers (runs S3 backup + anomaly analysis)
```bash
python src/consumers/main.py
```

---

## Anomaly Events in PostgreSQL

- Only `anomaly_events` insert is implemented; create the table first:
  ```sql
  CREATE TABLE IF NOT EXISTS anomaly_events (
    timestamp TIMESTAMPTZ,
    is_alert BOOLEAN,
    alert_type TEXT,
    alert_level TEXT,
    alert_title TEXT,
    alert_message TEXT,
    user_id TEXT,
    tags JSONB,
    metrics JSONB
  );
  ```
- DB connection uses `POSTGRES_*` env vars.

---

## TODO / Roadmap

- FastAPI: anomalies/events query APIs
- Dashboard: React + charts, hook to API/WS
- Docker: consumer/producer entrypoints, healthchecks, auto topic creation
- Testing: unit + integration and DB migrations
- Advanced detection: ML / Isolation Forest

# 📡 Real-Time Compliance / Anomaly Monitoring

Current status: three Kafka producers (logs/metrics/transactions) are working, two consumers (S3 backup + rule-based anomaly detection) are running, Discord alerts fire, and anomaly events are written to PostgreSQL. FastAPI REST API is implemented with dashboard and events endpoints. Docker Compose includes Kafka (KRaft), Postgres, API service, and dev containers.

---

## Status at a Glance

- ✅ Producers: randomized logs / metrics / transactions sent to Kafka
- ✅ Consumers:
  - `BackupS3Consumer`: save raw JSON to S3 (assume-role required)
  - `AnalysisConsumer`: per-type rules, Discord alerts, insert into Postgres `anomaly_events`
- ✅ Docker Compose: Kafka (KRaft), Postgres, API service, producer/consumer dev containers
- ✅ Database: Alembic migrations set up; initial migration creates `anomaly_events` table with `id` primary key
- ✅ FastAPI: REST API with dashboard and events modules
  - Dashboard endpoints: `/dashboard/overview`, `/dashboard/timeline`, `/dashboard/services`
  - Events endpoints: `/events`, `/events/{event_id}`, `/events/stats/summary`
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
4. FastAPI: REST API for querying anomaly events and dashboard statistics
   - Events API: query, filter, and paginate anomaly events
   - Dashboard API: overview statistics, alert timeline, service summaries

---

## Project Structure

```
src/
  producers/        # event generators + Kafka producer
  consumers/        # S3 backup, anomaly analysis, alerts, DB writes
  migrations/       # Alembic database migrations
  api/              # FastAPI REST API
    core/           # config, logging
    db/             # database session and models
    modules/        # dashboard and events modules
      dashboard/    # dashboard endpoints, service, repository
      events/       # events endpoints, service, repository
infra/
  docker/           # Dockerfile, docker-compose.yml, requirements
```

---

## Quickstart

### 1) Prepare `.env` (Kafka KRaft + service settings)

Copy the example environment file and fill in your values:

```bash
cp env.example infra/docker/.env
```

Edit `infra/docker/.env` with your configuration. Required keys:

- **Kafka (KRaft)**: `KAFKA_NODE_ID`, `KAFKA_PROCESS_ROLES`, `KAFKA_LISTENERS`, `KAFKA_ADVERTISED_LISTENERS`, `KAFKA_CONTROLLER_LISTENER_NAMES`, `KAFKA_LISTENER_SECURITY_PROTOCOL_MAP`, `KAFKA_CONTROLLER_QUORUM_VOTERS`, `KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR`, `KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR`, `KAFKA_TRANSACTION_STATE_LOG_MIN_ISR`, `KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS`, `KAFKA_NUM_PARTITIONS`
- **Pipeline**: `KAFKA_SERVER_1`, `AWS_REGION`, `S3_BUCKET`, `PREFIX`, `ROLE_ARN`, `DISCORD_WEBHOOK_URL`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- **API** (optional): `API_TITLE`, `API_VERSION`, `DEBUG`

For local testing, point Kafka/DB to `localhost`; leave Discord/S3 empty to avoid real calls. The API service will automatically connect to the `db` container when running in Docker Compose.

### 2) Start Kafka, Postgres, and API

```bash
docker compose -f infra/docker/docker-compose.yml up -d broker db api
```

Wait for services to be ready (especially Postgres healthcheck). The API will be available at `http://localhost:8000`.

### 3) Run Database Migrations

```bash
cd src
alembic upgrade head
```

This creates the `anomaly_events` table in PostgreSQL.

### 4) Start the Producer

```bash
python - <<'PY'
from producers import DataProducer
p = DataProducer(bootstrap_servers="localhost:9092")
p.start_data_stream(duration_seconds=120, interval_seconds=1)
PY
```

### 5) Start the Consumers (runs S3 backup + anomaly analysis)

```bash
python src/consumers/main.py
```

### 6) Access the API

The FastAPI service is available at:

- API: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs` (Swagger UI)
- Alternative Docs: `http://localhost:8000/redoc` (ReDoc)
- Health Check: `http://localhost:8000/health`

**Available Endpoints:**

- `GET /events` - List anomaly events with filtering and pagination
- `GET /events/{event_id}` - Get event by ID
- `GET /events/stats/summary` - Get event statistics
- `GET /dashboard/overview` - Get dashboard overview
- `GET /dashboard/timeline` - Get alert timeline
- `GET /dashboard/services` - Get service alert summary

---

## Anomaly Events in PostgreSQL

- The `anomaly_events` table is created automatically via Alembic migrations (see step 3 in Quickstart).
- Table schema:
  ```sql
  CREATE TABLE anomaly_events (
    id TEXT PRIMARY KEY,
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
- To create new migrations: `alembic revision --autogenerate -m "description"`
- To apply migrations: `alembic upgrade head`
- See `docs/MIGRATION_GUIDE.md` for detailed migration instructions.

---

## TODO / Roadmap

- Dashboard: React + charts, hook to API/WS
- Docker: consumer/producer entrypoints, healthchecks, auto topic creation
- Testing: unit + integration tests
- Advanced detection: ML / Isolation Forest

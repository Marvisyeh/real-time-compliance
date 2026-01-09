from sqlalchemy import Table, Column, MetaData
from sqlalchemy import Boolean, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData()

anomaly_events = Table(
    "anomaly_events",
    metadata,
    Column("timestamp", TIMESTAMP(timezone=True)),
    Column("is_alert", Boolean),
    Column("alert_type", Text),
    Column("alert_level", Text),
    Column("alert_title", Text),
    Column("alert_message", Text),
    Column("user_id", Text),
    Column("tags", JSONB),
    Column("metrics", JSONB),
)

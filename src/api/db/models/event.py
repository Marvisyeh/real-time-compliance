from sqlalchemy import Column, Boolean, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
import ulid

Base = declarative_base()


class AnomalyEvent(Base):
    __tablename__ = "anomaly_events"

    id = Column(Text, primary_key=True,
                default=lambda: ulid.new().str, index=True)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=True, index=True)
    is_alert = Column(Boolean, nullable=True, index=True)
    alert_type = Column(Text, nullable=True, index=True)
    alert_level = Column(Text, nullable=True)
    alert_title = Column(Text, nullable=True)
    alert_message = Column(Text, nullable=True)
    user_id = Column(Text, nullable=True, index=True)
    tags = Column(JSONB, nullable=True)
    metrics = Column(JSONB, nullable=True)

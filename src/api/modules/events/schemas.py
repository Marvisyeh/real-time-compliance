from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class AnomalyEventBase(BaseModel):
    timestamp: Optional[datetime] = None
    is_alert: Optional[bool] = None
    alert_type: Optional[str] = None
    alert_level: Optional[str] = None
    alert_title: Optional[str] = None
    alert_message: Optional[str] = None
    user_id: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None


class AnomalyEventCreate(AnomalyEventBase):
    pass


class AnomalyEventResponse(AnomalyEventBase):
    id: str

    class Config:
        from_attributes = True


class AnomalyEventFilter(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_alert: Optional[bool] = None
    alert_type: Optional[str] = None
    alert_level: Optional[str] = None
    user_id: Optional[str] = None
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)


class AnomalyEventStats(BaseModel):
    total_events: int
    alert_count: int
    alert_by_type: Dict[str, int]
    alert_by_level: Dict[str, int]

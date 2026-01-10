from datetime import datetime
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field


class TimeSeriesDataPoint(BaseModel):
    timestamp: datetime
    value: float


class AlertTrend(BaseModel):
    """alert trend data"""
    time_range: str
    alert_count: int
    total_count: int
    alert_rate: float


class ServiceAlertSummary(BaseModel):
    """service alert summary"""
    service: str
    total_alerts: int
    critical_alerts: int
    warning_alerts: int
    last_alert_time: Optional[datetime]


class DashboardOverview(BaseModel):
    """dashboard overview"""
    total_events: int
    total_alerts: int
    alert_rate: float
    alerts_by_type: Dict[str, int]
    alerts_by_level: Dict[str, int]
    recent_alerts: List[Dict[str, Any]]
    time_range: Dict[str, Optional[datetime]]


class AlertTimelineRequest(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    group_by: str = Field(default="hour", pattern="^(hour|day|week)$")
    alert_type: Optional[str] = None


class AlertTimelineResponse(BaseModel):
    timeline: List[AlertTrend]
    total_alerts: int
    peak_alert_time: Optional[datetime]

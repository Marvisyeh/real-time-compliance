from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime

from api.db.session import get_db
from api.modules.dashboard.service import DashboardService
from api.modules.dashboard.schemas import (
    DashboardOverview,
    AlertTimelineRequest,
    AlertTimelineResponse,
    ServiceAlertSummary
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview", response_model=DashboardOverview)
def get_overview(
    start_time: Optional[datetime] = Query(None, description="Start time"),
    end_time: Optional[datetime] = Query(None, description="End time"),
    db: Session = Depends(get_db)
):
    """get dashboard overview data"""
    service = DashboardService(db)
    return service.get_overview(start_time, end_time)


@router.get("/timeline", response_model=AlertTimelineResponse)
def get_alert_timeline(
    start_time: Optional[datetime] = Query(None, description="Start time"),
    end_time: Optional[datetime] = Query(None, description="End time"),
    group_by: str = Query(
        "hour", regex="^(hour|day|week)$", description="Group by"),
    alert_type: Optional[str] = Query(None, description="Alert type"),
    db: Session = Depends(get_db)
):
    """get alert timeline data"""
    service = DashboardService(db)
    request = AlertTimelineRequest(
        start_time=start_time,
        end_time=end_time,
        group_by=group_by,
        alert_type=alert_type
    )
    return service.get_alert_timeline(request)


@router.get("/services", response_model=List[ServiceAlertSummary])
def get_service_summary(
    start_time: Optional[datetime] = Query(None, description="Start time"),
    end_time: Optional[datetime] = Query(None, description="End time"),
    db: Session = Depends(get_db)
):
    """get service alert summary"""
    service = DashboardService(db)
    return service.get_service_summary(start_time, end_time)

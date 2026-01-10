from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from api.db.session import get_db
from api.modules.events.service import EventService
from api.modules.events.schemas import (
    AnomalyEventResponse,
    AnomalyEventFilter,
    AnomalyEventStats
)

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/{event_id}", response_model=AnomalyEventResponse)
def get_event(
    event_id: str,
    db: Session = Depends(get_db)
):
    """get event by id"""
    service = EventService(db)
    event = service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.get("", response_model=List[AnomalyEventResponse])
def list_events(
    start_time: Optional[datetime] = Query(None, description="Start time"),
    end_time: Optional[datetime] = Query(None, description="End time"),
    is_alert: Optional[bool] = Query(None, description="Is alert"),
    alert_type: Optional[str] = Query(None, description="Alert type"),
    alert_level: Optional[str] = Query(None, description="Alert level"),
    user_id: Optional[str] = Query(None, description="User ID"),
    limit: int = Query(100, ge=1, le=1000, description="Limit"),
    offset: int = Query(0, ge=0, description="Offset"),
    db: Session = Depends(get_db)
):
    """get event list (support filtering and pagination)"""
    filters = AnomalyEventFilter(
        start_time=start_time,
        end_time=end_time,
        is_alert=is_alert,
        alert_type=alert_type,
        alert_level=alert_level,
        user_id=user_id,
        limit=limit,
        offset=offset
    )
    service = EventService(db)
    return service.list_events(filters)


@router.get("/stats/summary", response_model=AnomalyEventStats)
def get_event_stats(
    start_time: Optional[datetime] = Query(None, description="Start time"),
    end_time: Optional[datetime] = Query(None, description="End time"),
    db: Session = Depends(get_db)
):
    """get event stats"""
    service = EventService(db)
    return service.get_event_stats(start_time, end_time)

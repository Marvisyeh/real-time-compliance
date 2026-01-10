from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from api.modules.events.repository import EventRepository
from api.modules.events.schemas import (
    AnomalyEventResponse,
    AnomalyEventFilter,
    AnomalyEventStats
)


class EventService:
    def __init__(self, db: Session):
        self.repository = EventRepository(db)

    def get_event(self, event_id: str) -> Optional[AnomalyEventResponse]:
        """get single event"""
        event = self.repository.get_by_id(event_id)
        if event:
            return AnomalyEventResponse.model_validate(event)
        return None

    def list_events(self, filters: AnomalyEventFilter) -> List[AnomalyEventResponse]:
        """get event list"""
        events = self.repository.get_all(filters)
        return [AnomalyEventResponse.model_validate(event) for event in events]

    def get_event_stats(self, start_time: Optional[datetime] = None,
                        end_time: Optional[datetime] = None) -> AnomalyEventStats:
        """get event stats"""
        stats = self.repository.get_stats(start_time, end_time)
        return AnomalyEventStats(**stats)


if __name__ == "__main__":
    from datetime import timedelta
    from api.db.session import get_db

    db = next(get_db())
    service = EventService(db)
    stats = service.get_event_stats(
        start_time=datetime.now() - timedelta(days=1), end_time=datetime.now())
    print(stats)

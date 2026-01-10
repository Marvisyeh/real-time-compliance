from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from api.modules.dashboard.repository import DashboardRepository
from api.modules.dashboard.schemas import (
    DashboardOverview,
    AlertTimelineRequest,
    AlertTimelineResponse,
    ServiceAlertSummary,
    AlertTrend
)


class DashboardService:
    def __init__(self, db: Session):
        self.repository = DashboardRepository(db)

    def get_overview(self, start_time: Optional[datetime] = None,
                     end_time: Optional[datetime] = None) -> DashboardOverview:
        """get dashboard overview"""
        data = self.repository.get_overview(start_time, end_time)
        return DashboardOverview(**data)

    def get_alert_timeline(self, request: AlertTimelineRequest) -> AlertTimelineResponse:
        """get alert timeline"""
        timeline_data = self.repository.get_alert_timeline(
            start_time=request.start_time,
            end_time=request.end_time,
            group_by=request.group_by,
            alert_type=request.alert_type
        )

        timeline = [AlertTrend(**item) for item in timeline_data]

        # find peak alert time
        peak_alert_time = None
        max_count = 0
        for item in timeline_data:
            if item["alert_count"] > max_count:
                max_count = item["alert_count"]
                if item["time_range"]:
                    peak_alert_time = datetime.fromisoformat(
                        item["time_range"])

        total_alerts = sum(item["alert_count"] for item in timeline_data)

        return AlertTimelineResponse(
            timeline=timeline,
            total_alerts=total_alerts,
            peak_alert_time=peak_alert_time
        )

    def get_service_summary(self, start_time: Optional[datetime] = None,
                            end_time: Optional[datetime] = None) -> List[ServiceAlertSummary]:
        """get service alert summary"""
        data = self.repository.get_service_summary(start_time, end_time)
        return [ServiceAlertSummary(**item) for item in data]


if __name__ == "__main__":
    from datetime import timedelta
    from api.db.session import get_db
    db = next(get_db())
    service = DashboardService(db)
    overview = service.get_overview(
        start_time=datetime.now() - timedelta(days=1), end_time=datetime.now())
    print(overview)

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from api.db.models.event import AnomalyEvent


class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_overview(self, start_time: Optional[datetime] = None,
                     end_time: Optional[datetime] = None) -> Dict[str, Any]:
        """get dashboard overview data"""
        query = self.db.query(AnomalyEvent)

        if start_time:
            query = query.filter(AnomalyEvent.timestamp >= start_time)
        if end_time:
            query = query.filter(AnomalyEvent.timestamp <= end_time)

        total_events = query.count()
        total_alerts = query.filter(AnomalyEvent.is_alert == True).count()
        alert_rate = (total_alerts / total_events *
                      100) if total_events > 0 else 0

        # count by alert type
        alerts_by_type = {}
        type_results = (
            query.filter(AnomalyEvent.is_alert == True)
            .filter(AnomalyEvent.alert_type.isnot(None))
            .with_entities(
                AnomalyEvent.alert_type,
                func.count(AnomalyEvent.id).label('count')
            )
            .group_by(AnomalyEvent.alert_type)
            .all()
        )
        for alert_type, count in type_results:
            alerts_by_type[alert_type] = count

        # count by alert level
        alerts_by_level = {}
        level_results = (
            query.filter(AnomalyEvent.is_alert == True)
            .filter(AnomalyEvent.alert_level.isnot(None))
            .with_entities(
                AnomalyEvent.alert_level,
                func.count(AnomalyEvent.id).label('count')
            )
            .group_by(AnomalyEvent.alert_level)
            .all()
        )
        for alert_level, count in level_results:
            alerts_by_level[alert_level] = count

        # recent alerts (last 10)
        recent_alerts = (
            query.filter(AnomalyEvent.is_alert == True)
            .order_by(AnomalyEvent.timestamp.desc())
            .limit(10)
            .all()
        )

        recent_alerts_data = []
        for alert in recent_alerts:
            recent_alerts_data.append({
                "id": alert.id,
                "timestamp": alert.timestamp.isoformat() if alert.timestamp else None,
                "alert_type": alert.alert_type,
                "alert_level": alert.alert_level,
                "alert_title": alert.alert_title,
                "alert_message": alert.alert_message,
                "user_id": alert.user_id
            })

        return {
            "total_events": total_events,
            "total_alerts": total_alerts,
            "alert_rate": round(alert_rate, 2),
            "alerts_by_type": alerts_by_type,
            "alerts_by_level": alerts_by_level,
            "recent_alerts": recent_alerts_data,
            "time_range": {
                "start": start_time.isoformat() if start_time else None,
                "end": end_time.isoformat() if end_time else None
            }
        }

    def get_alert_timeline(self, start_time: Optional[datetime] = None,
                           end_time: Optional[datetime] = None,
                           group_by: str = "hour",
                           alert_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """get alert timeline data"""
        query = self.db.query(AnomalyEvent).filter(
            AnomalyEvent.is_alert == True)

        if start_time:
            query = query.filter(AnomalyEvent.timestamp >= start_time)
        if end_time:
            query = query.filter(AnomalyEvent.timestamp <= end_time)
        if alert_type:
            query = query.filter(AnomalyEvent.alert_type == alert_type)

        # group by time
        if group_by == "hour":
            time_expr = func.date_trunc('hour', AnomalyEvent.timestamp)
        elif group_by == "day":
            time_expr = func.date_trunc('day', AnomalyEvent.timestamp)
        elif group_by == "week":
            time_expr = func.date_trunc('week', AnomalyEvent.timestamp)
        else:
            time_expr = func.date_trunc('hour', AnomalyEvent.timestamp)

        results = (
            query.with_entities(
                time_expr.label('time_bucket'),
                func.count(AnomalyEvent.id).label('alert_count'),
                func.count().over().label('total_count')
            )
            .group_by('time_bucket')
            .order_by('time_bucket')
            .all()
        )

        timeline = []
        total_count = query.count()
        for time_bucket, alert_count, _ in results:
            alert_rate = (alert_count / total_count *
                          100) if total_count > 0 else 0
            timeline.append({
                "time_range": time_bucket.isoformat() if time_bucket else None,
                "alert_count": alert_count,
                "total_count": total_count,
                "alert_rate": round(alert_rate, 2)
            })

        return timeline

    def get_service_summary(self, start_time: Optional[datetime] = None,
                            end_time: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """get service alert summary (extract service from tags)"""
        query = self.db.query(AnomalyEvent).filter(
            AnomalyEvent.is_alert == True)

        if start_time:
            query = query.filter(AnomalyEvent.timestamp >= start_time)
        if end_time:
            query = query.filter(AnomalyEvent.timestamp <= end_time)

        # get all alerts
        alerts = query.all()

        # count by service
        service_stats = {}
        for alert in alerts:
            service = "unknown"
            if alert.tags and isinstance(alert.tags, dict):
                service = alert.tags.get("service", "unknown")

            if service not in service_stats:
                service_stats[service] = {
                    "service": service,
                    "total_alerts": 0,
                    "critical_alerts": 0,
                    "warning_alerts": 0,
                    "last_alert_time": None
                }

            service_stats[service]["total_alerts"] += 1

            if alert.alert_level == "critical":
                service_stats[service]["critical_alerts"] += 1
            elif alert.alert_level == "warning":
                service_stats[service]["warning_alerts"] += 1

            if alert.timestamp:
                if (service_stats[service]["last_alert_time"] is None or
                        alert.timestamp > service_stats[service]["last_alert_time"]):
                    service_stats[service]["last_alert_time"] = alert.timestamp

        return list(service_stats.values())

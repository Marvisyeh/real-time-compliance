from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime

from api.db.models.event import AnomalyEvent
from api.modules.events.schemas import AnomalyEventFilter


class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, event_id: str) -> Optional[AnomalyEvent]:
        """根據 ID 獲取事件"""
        return self.db.query(AnomalyEvent).filter(AnomalyEvent.id == event_id).first()

    def get_all(self, filters: AnomalyEventFilter) -> List[AnomalyEvent]:
        """根據篩選條件獲取事件列表"""
        query = self.db.query(AnomalyEvent)

        # 應用篩選條件
        if filters.start_time:
            query = query.filter(AnomalyEvent.timestamp >= filters.start_time)
        if filters.end_time:
            query = query.filter(AnomalyEvent.timestamp <= filters.end_time)
        if filters.is_alert is not None:
            query = query.filter(AnomalyEvent.is_alert == filters.is_alert)
        if filters.alert_type:
            query = query.filter(AnomalyEvent.alert_type == filters.alert_type)
        if filters.alert_level:
            query = query.filter(
                AnomalyEvent.alert_level == filters.alert_level)
        if filters.user_id:
            query = query.filter(AnomalyEvent.user_id == filters.user_id)

        # 按時間倒序排列
        query = query.order_by(AnomalyEvent.timestamp.desc())

        # 分頁
        return query.offset(filters.offset).limit(filters.limit).all()

    def count(self, filters: AnomalyEventFilter) -> int:
        """計算符合條件的總數"""
        query = self.db.query(AnomalyEvent)

        if filters.start_time:
            query = query.filter(AnomalyEvent.timestamp >= filters.start_time)
        if filters.end_time:
            query = query.filter(AnomalyEvent.timestamp <= filters.end_time)
        if filters.is_alert is not None:
            query = query.filter(AnomalyEvent.is_alert == filters.is_alert)
        if filters.alert_type:
            query = query.filter(AnomalyEvent.alert_type == filters.alert_type)
        if filters.alert_level:
            query = query.filter(
                AnomalyEvent.alert_level == filters.alert_level)
        if filters.user_id:
            query = query.filter(AnomalyEvent.user_id == filters.user_id)

        return query.count()

    def get_stats(self, start_time: Optional[datetime] = None,
                  end_time: Optional[datetime] = None) -> dict:
        """獲取統計資訊"""
        query = self.db.query(AnomalyEvent)

        if start_time:
            query = query.filter(AnomalyEvent.timestamp >= start_time)
        if end_time:
            query = query.filter(AnomalyEvent.timestamp <= end_time)

        total_events = query.count()
        alert_count = query.filter(AnomalyEvent.is_alert == True).count()

        # 按類型統計
        alert_by_type = {}
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
            alert_by_type[alert_type] = count

        # 按級別統計
        alert_by_level = {}
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
            alert_by_level[alert_level] = count

        return {
            "total_events": total_events,
            "alert_count": alert_count,
            "alert_by_type": alert_by_type,
            "alert_by_level": alert_by_level
        }

from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from database.models import UserActivity
from domain_types import ActivityType

class UserActivityRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_activity(self, activity: UserActivity) -> UserActivity:
        self.session.add(activity)
        return activity

    def get_user_activities(self, user_id: str) -> List[UserActivity]:
        return self.session.query(UserActivity).filter(
            UserActivity.user_id == user_id
        ).order_by(UserActivity.timestamp).all()

    def get_recent_deposits(self, user_id: str, since: datetime) -> List[UserActivity]:
        return self.session.query(UserActivity).filter(
            UserActivity.user_id == user_id,
            UserActivity.activity_type == ActivityType.DEPOSIT.value,
            UserActivity.timestamp >= since
        ).all()

    def get_latest_timestamp(self, user_id: str) -> datetime:
        latest = self.session.query(UserActivity).filter(
            UserActivity.user_id == user_id
        ).order_by(UserActivity.timestamp.desc()).first()
        return latest.timestamp if latest else datetime.min 
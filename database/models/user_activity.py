from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLAlchemyEnum
from database.database import Base
from domain_types import ActivityType

class UserActivity(Base):
    __tablename__ = 'user_activities'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    activity_type = Column(SQLAlchemyEnum(ActivityType, values_callable=lambda x: [e.value for e in x]), nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
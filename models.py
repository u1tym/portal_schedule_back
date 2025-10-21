from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from .config import ScheduleBase

class ActivityCategory(ScheduleBase):
    __tablename__ = "activity_categories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class Schedule(ScheduleBase):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    is_all_day = Column(Boolean, default=False, nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)  # 分または日
    activity_category_id = Column(Integer, ForeignKey("activity_categories.id"), nullable=True)
    schedule_type = Column(String(50), nullable=True)
    location = Column(String(255), nullable=True)
    details = Column(Text, nullable=True)
    is_todo_completed = Column(Boolean, default=False, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    # リレーションシップ
    activity_category = relationship("ActivityCategory", back_populates="schedules")

# ActivityCategoryのリレーションシップを追加
ActivityCategory.schedules = relationship("Schedule", back_populates="activity_category")

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from .config import get_schedule_db
from ..account.config import get_account_db
from ..account.service import Account
from .models import Schedule, ActivityCategory

router = APIRouter()

class ScheduleRequest(BaseModel):
    username: str
    session_string: str

class ScheduleItem(BaseModel):
    id: int
    title: str
    is_all_day: bool
    start_datetime: datetime
    duration: int
    activity_category_id: Optional[int]
    schedule_type: Optional[str]
    location: Optional[str]
    details: Optional[str]
    is_todo_completed: bool

class ScheduleResponse(BaseModel):
    success: bool
    session_string: str
    schedules: List[ScheduleItem]

@router.post("/get-schedule", response_model=ScheduleResponse)
async def get_schedule(request: ScheduleRequest, schedule_db: Session = Depends(get_schedule_db), account_db: Session = Depends(get_account_db)):
    """スケジュール取得API"""
    # Accountインスタンス作成（アカウント用DBを使用）
    account = Account(request.username, account_db)

    # セッション確認
    if not account.verify_session(request.session_string):
        return ScheduleResponse(
            success=False,
            session_string="",
            schedules=[]
        )

    # セッション確認OKの場合、新しいセッション文字列を取得
    new_session_string = account.get_session_string()
    if not new_session_string:
        return ScheduleResponse(
            success=False,
            session_string="",
            schedules=[]
        )

    # ユーザーのスケジュールを取得
    schedules = schedule_db.query(Schedule).filter(
        Schedule.user_id == account.user_id,
        Schedule.is_deleted == False
    ).order_by(Schedule.start_datetime).all()

    # スケジュールデータを変換
    schedule_items = []
    for schedule in schedules:
        schedule_items.append(ScheduleItem(
            id=schedule.id,
            title=schedule.title,
            is_all_day=schedule.is_all_day,
            start_datetime=schedule.start_datetime,
            duration=schedule.duration,
            activity_category_id=schedule.activity_category_id,
            schedule_type=schedule.schedule_type,
            location=schedule.location,
            details=schedule.details,
            is_todo_completed=schedule.is_todo_completed
        ))

    return ScheduleResponse(
        success=True,
        session_string=new_session_string,
        schedules=schedule_items
    )

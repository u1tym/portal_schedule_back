from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .config import get_schedule_db
from ..account.config import get_account_db
from ..account.service import Account

router = APIRouter()

class ScheduleRequest(BaseModel):
    username: str
    hash_value: str

class ScheduleResponse(BaseModel):
    success: bool
    hash_value: str

@router.post("/get-schedule", response_model=ScheduleResponse)
async def get_schedule(request: ScheduleRequest, schedule_db: Session = Depends(get_schedule_db), account_db: Session = Depends(get_account_db)):
    """スケジュール取得API"""
    # Accountインスタンス作成（アカウント用DBを使用）
    account = Account(request.username, account_db)

    # セッション確認
    if not account.verify_session(request.hash_value):
        return ScheduleResponse(
            success=False,
            hash_value=""
        )

    # セッション確認OKの場合、新しいセッション文字列を取得
    new_session_string = account.get_session_string()
    if not new_session_string:
        return ScheduleResponse(
            success=False,
            hash_value=""
        )

    return ScheduleResponse(
        success=True,
        hash_value=new_session_string
    )

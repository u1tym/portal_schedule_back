from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..core.database import get_db
from ..account.service import Account

router = APIRouter()

class ScheduleRequest(BaseModel):
    username: str
    hash_value: str

class ScheduleResponse(BaseModel):
    success: bool
    hash_value: str

@router.post("/get-schedule", response_model=ScheduleResponse)
async def get_schedule(request: ScheduleRequest, db: Session = Depends(get_db)):
    """スケジュール取得API"""
    # Accountインスタンス作成
    account = Account(request.username, db)

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

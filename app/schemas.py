from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class SkinBase(BaseModel):
    name: str
    emoji: str
    price: int
    color: int

class SkinResponse(SkinBase):
    id: int
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    coins: int
    current_level: int
    streak_days: int 

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

class GameFinish(BaseModel):
    level: int
    score: int

class MessageItem(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[MessageItem]
    language: str # 'kz', 'ru' или 'en'
    child_age: int | None = None      
    child_gender: str | None = None   
    parent_goal: str | None = None

class ChatResponse(BaseModel):
    reply: str

class ActionLogResponse(BaseModel):
    emoji: str
    action_kz: str
    action_ru: str
    action_en: Optional[str] = None # <-- ДОБАВИЛИ АНГЛИЙСКИЙ (Optional, чтобы старые логи не ломались)
    created_at: datetime

    class Config:
        from_attributes = True

class AnalyticsResponse(BaseModel):
    total_minutes: int
    weekly_minutes: List[int] 
    recent_actions: List[ActionLogResponse]
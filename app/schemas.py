from typing import List

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
    language: str# Будем передавать 'kz' или 'ru', чтобы ИИ знал, на каком языке отвечать
    child_age: int | None = None      # Возраст
    child_gender: str | None = None   # 'boy' или 'girl'
    parent_goal: str | None = None

class ChatResponse(BaseModel):
    reply: str
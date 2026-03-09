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


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class GameFinish(BaseModel):
    level: int
    score: int

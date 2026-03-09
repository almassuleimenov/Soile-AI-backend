from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas, database

router = APIRouter(prefix="/api/game", tags=["Game"])

@router.post("/finish", response_model=schemas.UserResponse)
async def finish_level(game_data: schemas.GameFinish, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.User).where(models.User.id == 1))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.coins += game_data.score
    if game_data.level >= user.current_level:
        user.current_level = game_data.level + 1

    await db.commit()
    await db.refresh(user)
    
    return user
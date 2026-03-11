from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas, database

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/me", response_model=schemas.UserResponse)
async def get_current_user(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.User).where(models.User.id == 1))
    user = result.scalars().first()
    
    today = date.today()

    if not user:
        user = models.User(
            name="Батыр", 
            coins=100, 
            current_level=1, 
            streak_days=1, 
            last_login=today
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    else:
        if user.last_login != today:
            if user.last_login == today - timedelta(days=1):
                user.streak_days += 1
            else:
                user.streak_days = 1
                
            user.last_login = today
            await db.commit()
            await db.refresh(user)

    return user
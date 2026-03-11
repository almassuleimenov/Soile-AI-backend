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

from sqlalchemy import desc

# ... твой код get_current_user ...

@router.get("/analytics", response_model=schemas.AnalyticsResponse)
async def get_analytics(db: AsyncSession = Depends(database.get_db)):
    logs_result = await db.execute(
        select(models.ActionLog)
        .where(models.ActionLog.user_id == 1)
        .order_by(desc(models.ActionLog.created_at))
        .limit(5)
    )
    recent_logs = logs_result.scalars().all()

    total_logs_result = await db.execute(select(models.ActionLog).where(models.ActionLog.user_id == 1))
    total_logs = len(total_logs_result.scalars().all())
    total_time = total_logs * 5 
    
    weekly = [15, 30, 10, 45, 20, 15, min(total_time, 50)]

    return schemas.AnalyticsResponse(
        total_minutes=total_time,
        weekly_minutes=weekly,
        recent_actions=recent_logs
    )
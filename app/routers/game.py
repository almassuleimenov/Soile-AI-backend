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

    # ЗАПИСЫВАЕМ ДЕЙСТВИЕ В ИСТОРИЮ
    # Внимание: если в таблице ActionLog еще нет колонки action_en, 
    # SQLAlchemy может выдать ошибку. Если выдаст - просто удали строку action_en.
    new_log = models.ActionLog(
        user_id=user.id,
        emoji="🗣️",
        action_kz=f"{game_data.level}-ші деңгейді сәтті аяқтады",
        action_ru=f"Успешно пройден уровень {game_data.level}",
        # action_en=f"Successfully completed level {game_data.level}" # <-- Раскомментируй, когда добавишь в models.py
    )
    db.add(new_log)

    await db.commit()
    await db.refresh(user)
    return user
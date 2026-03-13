from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app import models, schemas, database

router = APIRouter(prefix="/api/shop", tags=["Shop"])

DEFAULT_SKINS = [
    {"name": "Ковбой", "emoji": "🤠", "price": 50, "color": 0xFFFFF3E0},
    {"name": "Ниндзя", "emoji": "🥷", "price": 100, "color": 0xFFECEFF1},
    {"name": "Космонавт", "emoji": "🧑‍🚀", "price": 150, "color": 0xFFEDE7F6},
    {"name": "Маг", "emoji": "🧙‍♂️", "price": 200, "color": 0xFFE8F5E9},
    {"name": "Пират", "emoji": "🏴‍☠️", "price": 300, "color": 0xFFFFEBEE},
    {"name": "Король", "emoji": "🤴", "price": 500, "color": 0xFFFFF9C4},
]


@router.get("/skins", response_model=List[schemas.SkinResponse])
async def get_all_skins(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.Skin))
    skins = result.scalars().all()

    if not skins:
        for skin_data in DEFAULT_SKINS:
            new_skin = models.Skin(**skin_data)
            db.add(new_skin)
        await db.commit()

        result = await db.execute(select(models.Skin))
        skins = result.scalars().all()

    return skins


@router.post("/buy/{skin_id}")
async def buy_skin(skin_id: int, db: AsyncSession = Depends(database.get_db)):
    user_result = await db.execute(select(models.User).where(models.User.id == 1))
    user = user_result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    skin_result = await db.execute(select(models.Skin).where(models.Skin.id == skin_id))
    skin = skin_result.scalars().first()

    if not skin:
        raise HTTPException(status_code=404, detail="Skin not found")

    existing_purchase = await db.execute(
        select(models.UserSkin)
        .where(models.UserSkin.user_id == user.id)
        .where(models.UserSkin.skin_id == skin.id)
    )
    if existing_purchase.scalars().first():
        raise HTTPException(status_code=400, detail="Skin already purchased")

    if user.coins < skin.price:
        raise HTTPException(status_code=400, detail="Not enough coins")

    user.coins -= skin.price
    user_skin = models.UserSkin(user_id=user.id, skin_id=skin.id)
    db.add(user_skin)
    
    new_log = models.ActionLog(
        user_id=user.id,
        emoji="🛒",
        action_kz=f"'{skin.name}' скинін сатып алды",
        action_ru=f"Покупка скина '{skin.name}'",
        # action_en=f"Purchased skin '{skin.name}'" # <-- Раскомментируй, когда добавишь в models.py
    )
    db.add(new_log)

    await db.commit()

    return {"message": "Success", "coins_left": user.coins}
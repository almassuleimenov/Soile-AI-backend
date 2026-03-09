from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="Батыр")
    coins = Column(Integer, default=100)
    current_level = Column(Integer, default=1)

    skins = relationship("UserSkin", back_populates="user")


class Skin(Base):
    __tablename__ = "skins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    emoji = Column(String)
    price = Column(Integer)
    color = Column(BigInteger)


class UserSkin(Base):
    __tablename__ = "user_skins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skin_id = Column(Integer, ForeignKey("skins.id"))

    user = relationship("User", back_populates="skins")

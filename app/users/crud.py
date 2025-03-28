# app/users/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.users import models, schemas
from app.core.security import hash_password, verify_password
from app.users.models import User


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_pw = hash_password(user.password)
    name = user.name or user.email.split("@")[0]
    db_user = models.User(
        name = name,
        email=user.email,
        password=hashed_pw
    )
    db.add(db_user)
    await db.commit()
    return db_user


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
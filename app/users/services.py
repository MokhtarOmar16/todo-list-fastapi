from app.users import crud, schemas
from app.core.security import create_access_token, create_refresh_token
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

async def register_user(db: AsyncSession, user_data: schemas.UserCreate):
    user = await crud.get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    new_user = await crud.create_user(db, user_data)
    return new_user

async def login_user(db: AsyncSession, user_data: schemas.UserLogin):
    user = await crud.authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})


    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

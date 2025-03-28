from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.users import schemas, crud
from app.core.security import create_access_token, create_refresh_token, verify_token
from app.api.deps import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=schemas.UserRead)
async def signup(user_data: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await crud.create_user(db, user_data)
    return new_user

@router.post("/login", response_model=schemas.Token)
async def login(user_data: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    user = await crud.authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# تجديد التوكن
@router.post("/refresh", response_model=schemas.Token)
async def refresh_token(request: schemas.RefreshTokenRequest):
    payload = verify_token(request.refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    email = payload.get("sub")
    access_token = create_access_token(data={"sub": email})
    refresh_token = create_refresh_token(data={"sub": email})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

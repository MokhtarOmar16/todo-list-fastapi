from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.users import schemas, services
from app.core.security import verify_token
from app.api.deps import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=schemas.UserRead)
async def signup(user_data: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await services.register_user(db, user_data)

@router.post("/login", response_model=schemas.Token)
async def login(user_data: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    return await services.login_user(db, user_data)

@router.post("/refresh")
async def refresh_token(request: schemas.RefreshTokenRequest):
    payload = verify_token(request.refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user_id = payload.get("sub")
    access_token = services.create_access_token(data={"sub": str(user_id)})

    return {
        "access_token": access_token,
    }
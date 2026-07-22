from fastapi import APIRouter, Depends
from schemas.auth import RegisterRequest, LoginRequest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from security import (
    hash_password,
    verify_password,
    create_access_token
)

from database import get_db
from models.user import User

router = APIRouter()

fake_db = {}

@router.post("/register")
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(User).where(User.email == data.email)
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        return {"message": "User already exists"}

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password)
    )

    db.add(user)

    await db.commit()

    await db.refresh(user)

    token = create_access_token(str(user.id))

    return {
        "access_token": token,
        "message": "Successful"
    }




@router.post("/login")
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(User).where(User.email == data.email)
    )

    user = result.scalar_one_or_none()

    if not user:
        return {"message": "Invalid credentials"}

    if not verify_password(
        data.password,
        user.password_hash
    ):
        return {"message": "Invalid credentials"}

    token = create_access_token(str(user.id))

    return {
        "access_token": token,
        "user_id": str(user.id)
    }
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import SessionLocal
from Models.models import User
from Schemas.schemas_users import UpdateUserSchema
from typing import List
from Authorization import get_current_user
from Blacklist import blacklist_token

routerUser = APIRouter()


# Get session from the Database
async def get_session_db():
    async with SessionLocal() as session:
        yield session


# Update User
@routerUser.put("/User", response_model=List[UpdateUserSchema])
async def updateUser(
    user: UpdateUserSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_db),
):
    result = await db.execute(select(User).filter(User.id == current_user.id))
    existing_user = result.scalars().first()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.dict().items():
        setattr(existing_user, key, value)

    await db.commit()
    await db.refresh(existing_user)
    return [existing_user]


# remove User
@routerUser.delete("/User")
async def removeUser(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session_db),
):
    result = await db.execute(select(User).filter(User.id == current_user.id))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    blacklist_token(current_user.password_hash)
    return {"msg": "User has been removed"}

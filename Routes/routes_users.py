from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import SessionLocal
from Models.models import User
from Schemas.schemas_users import UserSchema, AddUpdateUserSchema
from typing import List

routerUser = APIRouter()


# Get session from the Database
async def get_session_db():
    async with SessionLocal() as session:
        yield session


# Get All Users
@routerUser.get("/Users", response_model=List[UserSchema])
async def getAllUsers(db: AsyncSession = Depends(get_session_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


# Get Specific User
@routerUser.get("/Users/{User_id}", response_model=List[UserSchema])
async def getUser(User_id: int, db: AsyncSession = Depends(get_session_db)):
    result = await db.execute(select(User).filter(User.id == User_id))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return [user]


# Add User
@routerUser.post("/Users", response_model=List[AddUpdateUserSchema])
async def addUser(
    user: AddUpdateUserSchema, db: AsyncSession = Depends(get_session_db)
):

    newUser = User(**user.dict())
    db.add(newUser)
    await db.commit()
    await db.refresh(newUser)
    return [newUser]


# Update User
@routerUser.put("/Users/{User_id}", response_model=List[AddUpdateUserSchema])
async def updateUser(
    User_id: int, user: AddUpdateUserSchema, db: AsyncSession = Depends(get_session_db)
):
    result = await db.execute(select(User).filter(User.id == User_id))
    existing_user = result.scalars().first()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.dict().items():
        setattr(existing_user, key, value)

    await db.commit()
    await db.refresh(existing_user)
    return [existing_user]

# remove User
@routerUser.delete("/Users/{User_id}", response_model=List[UserSchema])
async def removeUser(User_id: int, db: AsyncSession = Depends(get_session_db)):
    result = await db.execute(select(User).filter(User.id == User_id))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return [user]

#remove all users
@routerUser.delete("/Users", response_model=List[UserSchema])
async def removeUsers(db: AsyncSession = Depends(get_session_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    
    for user in users:
        await db.delete(user)
        await db.commit()
    return users
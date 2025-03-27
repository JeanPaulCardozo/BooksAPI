from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from database import SessionLocal
from Models.models import User
from Schemas.schemas_users import UserSchema
from Blacklist import is_token_blacklisted
from dotenv import load_dotenv
import os

filename = "Credentials.env"
load_dotenv(filename)

# Setting JWT
SECRET_KEY = os.getenv("AUTHORIZATION_SECRET_KEY")
ALGORITHM = os.getenv("AUTHORIZATION_ALGORITHM")
ENCRYPT_SCHEMA = os.getenv("ENCRYPT_SCHEMA")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Encrypt password
pwd_context = CryptContext(schemes=[ENCRYPT_SCHEMA], deprecated="auto")

# Authorization with OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# Get session from the Database
async def get_session_db():
    async with SessionLocal() as session:
        yield session


# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Encrypt password
def get_password_hash(password):
    return pwd_context.hash(password)


# Create access token witn JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Create Rounter with FastAPI
router = APIRouter()


# Add User
@router.post("/register")
async def register(user_data: UserSchema, db: AsyncSession = Depends(get_session_db)):
    # Verify user exist
    result = await db.execute(select(User).filter(User.email == user_data.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Encrypt password
    hashed_password = get_password_hash(user_data.password)

    # Add User
    new_user = User(
        name=user_data.name, email=user_data.email, password_hash=hashed_password
    )
    db.add(new_user)
    await db.commit()

    return {"msg": "User registered successfully"}


# Login
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session_db),
):
    result = await db.execute(select(User).filter(User.email == form_data.username))
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# Middleware to protect routes
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session_db)
):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401, detail="Token invalid or expired")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        result = await db.execute(select(User).filter(User.email == email))
        user = result.scalars().first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

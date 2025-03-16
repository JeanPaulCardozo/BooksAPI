from database import Base, engine
import asyncio
from fastapi import FastAPI
from routes import router

app = FastAPI()

app.include_router(router)

#Create the database tables in postgresql
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to BooksAPI with PostgreSQL"}





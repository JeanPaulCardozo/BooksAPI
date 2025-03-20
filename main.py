from database import Base, engine
from fastapi import FastAPI
from Routes.routes_books import routerBook
from Routes.routes_users import routerUser

app = FastAPI()

app.include_router(routerUser, prefix="/Users", tags=["Users"])
app.include_router(routerBook, prefix="/Books", tags=["Books"])


# Create the database tables in postgresql
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.get("/")
async def root():
    return {"message": "Welcome to BooksAPI with PostgreSQL"}

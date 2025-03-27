from database import Base, engine
from fastapi import FastAPI
from Routes.routes_books import routerBook
from Routes.routes_users import routerUser
from Authorization import router

app = FastAPI()

app.include_router(routerUser, tags=["Users"])
app.include_router(routerBook, tags=["Books"])
app.include_router(router, tags=["Authorization"])


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

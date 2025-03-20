from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import SessionLocal
from Models.models import Book, User
from Schemas.schemas_books import BookSchema, AddUpdateBookSchema
from typing import List

routerBook = APIRouter()


# Get session from the Database
async def get_session_db():
    async with SessionLocal() as session:
        yield session


# Get All Books
@routerBook.get("/Users/{User_id}/Books", response_model=List[BookSchema])
async def getBooks(User_id: int, db: AsyncSession = Depends(get_session_db)):
    result = await db.execute(select(Book).filter(Book.user_id == User_id))
    books = result.scalars().all()
    return books


# Get Specific Book
@routerBook.get("/Users/{User_id}/Books/{Book_id}", response_model=BookSchema)
async def getBook(
    User_id: int, Book_id: int, db: AsyncSession = Depends(get_session_db)
):
    result = await db.execute(
        select(Book).filter(Book.user_id == User_id, Book.id == Book_id)
    )
    book = result.scalars().first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# Remove a Book
@routerBook.delete("/Users/{User_id}/Books/{Book_id}", response_model=List[BookSchema])
async def RemoveBook(
    User_id: int, Book_id: int, db: AsyncSession = Depends(get_session_db)
):
    result = await db.execute(
        select(Book).filter(Book.user_id == User_id, Book.id == Book_id)
    )
    book = result.scalars().first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    await db.delete(book)
    await db.commit()
    return [book]


# Add a Book
@routerBook.post("/Users/{User_id}/Books", response_model=List[AddUpdateBookSchema])
async def AddBook(
    User_id: int, book: AddUpdateBookSchema, db: AsyncSession = Depends(get_session_db)
):
    result = await db.execute(select(User).filter(User.id == User_id))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    newBook = Book(**book.dict(), user_id=User_id)
    db.add(newBook)
    await db.commit()
    await db.refresh(newBook)
    return [newBook]


# Update a Book
@routerBook.put(
    "/Users/{User_id}/Books/{Book_id}", response_model=List[AddUpdateBookSchema]
)
async def UpdateBook(
    User_id: int,
    Book_id: int,
    book: AddUpdateBookSchema,
    db: AsyncSession = Depends(get_session_db),
):
    result = await db.execute(
        select(Book).filter(Book.user_id == User_id, Book.id == Book_id)
    )
    existingBook = result.scalars().first()

    if existingBook is None:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book.dict().items():
        setattr(existingBook, key, value)

    await db.commit()
    await db.refresh(existingBook)
    return [existingBook]


# Remove All Books from a User
@routerBook.delete("Users/{User_id}/Books", response_model=List[BookSchema])
async def RemoveAllBooks(User_id: int, db: AsyncSession = Depends(get_session_db)):
    result = await db.execute(select(Book).filter(Book.user_id == User_id))
    books = result.scalars().all()

    if books is None:
        raise HTTPException(status_code=404, detail="Books not found")

    for book in books:
        await db.delete(book)
        await db.commit()
    return books

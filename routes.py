from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import SessionLocal
from models import Book
from schemas import BookSchema, AddUpdateBookSchema
from typing import List

router = APIRouter()


# Get session from the Database
async def get_session_db():
    async with SessionLocal() as session:
        yield session


# Get All Books
@router.get("/Books", response_model=List[BookSchema])
async def getBooks(db: AsyncSession = Depends(get_session_db)):
    result = await db.execute(select(Book))
    books = result.scalars().all()
    return books


# Get Specific Book
@router.get("/Books/{Book_id}", response_model=BookSchema)
async def getBook(Book_id: int, db: AsyncSession = Depends(get_session_db)):
    result = await db.execute(select(Book).filter(Book.id == Book_id))
    book = result.scalars().first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# Remove a Book
@router.delete("/Books/{Book_id}", response_model=List[BookSchema])
async def RemoveBook(Book_id: int, db: AsyncSession = Depends(get_session_db)):
    result = await db.execute(select(Book).filter(Book.id == Book_id))
    book = result.scalars().first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    await db.delete(book)
    await db.commit()
    return [book]


# Add a Book
@router.post("/Books", response_model=List[AddUpdateBookSchema])
async def AddBook(book: AddUpdateBookSchema, db: AsyncSession = Depends(get_session_db)):
    newBook = Book(**book.dict())
    db.add(newBook)
    await db.commit()
    await db.refresh(newBook)
    return [newBook]


# Update a Book
@router.put("/Books/{Book_id}", response_model=List[AddUpdateBookSchema])
async def UpdateBook(
    Book_id: int, book: AddUpdateBookSchema, db: AsyncSession = Depends(get_session_db)
):
    result = await db.execute(select(Book).filter(Book.id == Book_id))
    existingBook = result.scalars().first()

    if existingBook is None:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book.dict().items():
        setattr(existingBook, key, value)

    await db.commit()
    await db.refresh(existingBook)
    return [existingBook]

#Remove All Books
@router.delete("/Books", response_model=List[BookSchema])
async def RemoveAllBooks(db: AsyncSession = Depends(get_session_db)):
    result = await db.execute(select(Book))
    books = result.scalars().all()
    
    if books is None:
        raise HTTPException(status_code=404, detail="Books not found")
    
    for book in books:
        await db.delete(book)
        await db.commit()
    return books
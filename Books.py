from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


# Data Model
class Book(BaseModel):
    id: int
    Title: str
    Description: Optional[str] = None
    Author: str
    Price: float
    YearRelease: int


# Database
BooksDB = [
    {"id": 1, "Title": "My Book", "Author": "Me", "Price": "0.00", "YearRelease": 2021}
]


# Get All Books
@app.get("/Books", response_model=List[Book])
def getBooks():
    return BooksDB


# Get Specific Book
@app.get("/Books/{Book_id}", response_model=Book)
def getBook(Book_id: int):
    for book in BooksDB:
        if book["id"] == Book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


# Remove a Book
@app.delete("/Books/{Book_id}", response_model=List[Book])
def RemoveBook(Book_id: int):
    for book in BooksDB:
        if book["id"] == Book_id:
            BooksDB.remove(book)
            return BooksDB, {"message": "Book removed successfully"}

    raise HTTPException(status_code=404, detail="Book not found")


# Add a Book
@app.post("/Books", response_model=List[Book])
def AddBook(book: Book):
    BooksDB.append(book)
    return BooksDB


# Update a Book
@app.put("/Books/{Book_id}", response_model=List[Book])
def UpdateBook(Book_id: int, book: Book):
    for index, book in enumerate(BooksDB):
        if book["id"] == Book_id:
            BooksDB[index] = book
            return BooksDB
    raise HTTPException(status_code=404, detail="Book not found")

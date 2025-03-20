from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)

    books = relationship("Book", back_populates="user")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    author = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    yearrelease = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="books")

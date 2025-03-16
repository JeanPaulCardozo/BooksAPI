from sqlalchemy import Column, Integer, String, Numeric
from database import Base


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    author = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    yearrelease = Column(Integer, nullable=False)

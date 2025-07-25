from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import declarative_base
from enum import Enum

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    dob = Column(Date)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, nullable=False, unique=True)

    def __str__(self):
        return f"[{self.id}] - {self.title} by {self.author}, {self.isbn}"

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
        }


class BookCopyStatus(str, Enum):
    AVAILABLE = "available"
    LOANED = "loaned"
    LOST = "lost"


class BookCopy(Base):
    __tablename__ = "book_copies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    status = Column(SQLEnum(BookCopyStatus), nullable=False)


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_copy_id = Column(Integer, ForeignKey("book_copies.id"))
    loan_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)

from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.models import Book


def add_book_to_db(session: Session, title: str, author: str, isbn: str) -> Book:
    book = Book(title=title, author=author, isbn=isbn)
    session.add(book)
    session.commit()

    return book


def get_book_by_isbn_from_db(session: Session, isbn: str) -> Book:
    selection = select(Book).where(Book.isbn == isbn)
    book = session.execute(selection).scalar()

    return book


def get_book_by_id_from_db(session: Session, book_id: int) -> Book:
    selection = select(Book).where(Book.id == book_id)
    book = session.execute(selection).scalar()

    return book


def get_all_books_from_db(session: Session) -> List[Book]:
    selection = select(Book)
    books = list(session.execute(selection).scalars().all())

    return books

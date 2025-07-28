from werkzeug.routing import ValidationError

from repositories.book_copy_repository import *
from repositories.book_repository import *


def add_book_with_copy(session: Session, title: str, author: str, isbn: str):
    book = get_book_by_isbn_from_db(session, isbn)
    if book:
        raise ValidationError(f"Book with isbn {isbn} already exists - id: {book.id}.")

    book = add_book_to_db(session, title=title, author=author, isbn=isbn)
    add_book_copy_to_db(session, book.id)

    return book


def get_all_books(session: Session) -> List[Book]:
    books = get_all_books_from_db(session)
    return books


def get_book_by_id(session: Session, book_id: int) -> Book:
    book = get_book_by_id_from_db(session, book_id)
    if not book:
        raise ValidationError(f"Book with id {book_id} does not exist.")

    return book

from sqlalchemy.orm import Session
from models.models import BookCopy, BookCopyStatus


def add_book_copy_to_db(session: Session, book_id: int) -> BookCopy:
    book_copy = BookCopy(book_id=book_id, status=BookCopyStatus.AVAILABLE)
    session.add(book_copy)
    session.commit()

    return book_copy

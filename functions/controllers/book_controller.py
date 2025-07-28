import json

from azure.functions import HttpResponse

from services.book_service import *


class BookController:
    def __init__(self, SessionLocal):
        self.SessionLocal = SessionLocal

    def get_books(self):
        with self.SessionLocal() as session:
            books = get_all_books(session)

        if books:
            output = json.dumps([book.to_json() for book in books], indent=4)
            return HttpResponse(output, status_code=200)

        return HttpResponse(f"No books found.", status_code=200)

    def get_book(self, book_id: int):
        try:
            with self.SessionLocal() as session:
                book = get_book_by_id(session, book_id)

            output = json.dumps(book.to_json(), indent=4)
            return HttpResponse(output, status_code=200)

        except ValidationError as e:
            return HttpResponse(repr(e), status_code=400)

    def add_book(self, title: str, author: str, isbn: str):
        try:
            with self.SessionLocal() as session:
                add_book_with_copy(session, title, author, isbn)

            return HttpResponse(
                f"Book [{title} by {author}, ISBN = {isbn}] added successfully!",
                status_code=200
            )
        except (TypeError, ValueError) as e:
            return HttpResponse(repr(e), status_code=400)

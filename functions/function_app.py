import logging
import os

import azure.functions as func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from controllers.book_controller import BookController
from decorators.validators import validate_request_params

app = func.FunctionApp()

engine = create_engine(os.environ["DB_URL"], echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@app.route(route="add-book", methods=["POST"])
@validate_request_params(
    title={"type": str, "required": True},
    author={"type": str, "required": True},
    isbn={"type": str, "required": True},
)
def add_book(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    title = req_body.get('title')
    author = req_body.get('author')
    isbn = req_body.get('isbn')

    book_controller = BookController(SessionLocal)
    logging.info(f"[add-book] Processing POST request. Title: {title}, author: {author}, isbn: {isbn}")

    return book_controller.add_book(title, author, isbn)


@app.route(route="books", methods=["GET"])
@validate_request_params(
    id={"type": int, "required": False},
)
def get_books(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
    except ValueError:
        req_body = {}

    book_id = req_body.get('id')

    book_controller = BookController(SessionLocal)
    logging.info(f"[books] Processing GET request.")

    if book_id:
        return book_controller.get_book(book_id)

    return book_controller.get_books()

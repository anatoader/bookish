import azure.functions as func
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from services.book_service import *
import json

app = func.FunctionApp()

engine = create_engine(os.environ["DB_URL"], echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@app.route(route="add-book", methods=["POST"])
def add_book(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        title = req_body.get('title')
        author = req_body.get('author')
        isbn = req_body.get('isbn')

        with SessionLocal() as session:
            add_book_with_copy(session, title, author, isbn)

        logging.info(f"[add-book] Processing POST request. Title: {title}")

        return func.HttpResponse(
            f"Book [{title} by {author}, ISBN = {isbn}] added successfully!",
            status_code=200
        )
    except ValueError as e:
        return func.HttpResponse(repr(e), status_code=400)


@app.route(route="books", methods=["GET"])
def get_books(req: func.HttpRequest) -> func.HttpResponse:
    with SessionLocal() as session:
        books = get_all_books(session)

    logging.info(f"[books] Processing GET request.")

    if books:
        output = json.dumps([book.to_json() for book in books], indent=4)
        return func.HttpResponse(output, status_code=200)

    return func.HttpResponse(f"No book copies found", status_code=200)

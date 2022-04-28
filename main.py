from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

import os
from dotenv import load_dotenv
from schema import Book as SchemaBook
from schema import Author as SchemaAuthor
from models import Book as ModelBook
from models import Author as ModelAuthor

load_dotenv(".env")
app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

@app.get(path="/")
async def home():
    return {"message":"Hola World"}

@app.post(path="/add-book",response_model=SchemaBook)
async def add_book(book:SchemaBook):
    db_book = ModelBook(title=book.title,rating=book.rating,author_id=book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book

@app.post(path="/add-author",response_model=SchemaAuthor)
async def add_book(author:SchemaAuthor):
    db_author = ModelAuthor(name=author.name, age=author.age)
    db.session.add(db_author)
    db.session.commit()
    return db_author

@app.get("/books")
def get_books():
    books = db.session.query(ModelBook).all()
    return books

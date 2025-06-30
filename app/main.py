from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, engine
from app.cache import get_books_from_cache, set_books_to_cache

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(title=book.title, author=book.author)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books", response_model=list[schemas.Book])
def get_books(db: Session = Depends(get_db)):
    cached_books = get_books_from_cache()
    if cached_books:
        return cached_books
    books = db.query(models.Book).all()
    result = [schemas.Book.from_orm(book).model_dump() for book in books]
    set_books_to_cache(result)
    return result

@app.post("/books/{book_id}/reviews", response_model=schemas.Review)
def add_review(book_id: int, review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_review = models.Review(content=review.content, rating=review.rating, book_id=book_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@app.get("/books/{book_id}/reviews", response_model=list[schemas.Review])
def get_reviews(book_id: int, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).filter(models.Review.book_id == book_id).all()
    return reviews

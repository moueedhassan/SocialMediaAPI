import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import time
from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db
from .schemas import Post, PostBase, PostCreate


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='', database='',
                                user='', password="", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesful!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error", error)
        time.sleep(2)


@app.get("/")
async def root():
    return {"message": "Welcome to my API!"}


@app.get("/posts", response_model=List[Post])
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts") -- raw SQL
    # posts = cursor.fetchall()
    posts = db.query(Post).all()
    return posts


@app.post("/createposts", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):

    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # store it back into the variable

    return new_post


@app.get("/posts/{id}", response_model=Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=Post)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()




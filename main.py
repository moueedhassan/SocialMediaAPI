import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import time
from myapp.models import Base
from sqlalchemy.orm import Session
from myapp.database import engine, get_db
from myapp.schemas import Post, PostBase, PostCreate, UserCreate
from myapp import models, schemas, utils
from passlib.context import CryptContext
from myapp.routers import post, user, auth


pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password="Allah7866", cursor_factory=RealDictCursor)
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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

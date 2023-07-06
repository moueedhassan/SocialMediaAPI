from fastapi import FastAPI
from myapp.models import Base
from myapp.database import engine
from myapp.routers import post, user, auth
from myapp.config import Settings

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to my API!"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

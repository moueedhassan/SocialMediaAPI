from fastapi import FastAPI
from myapp.models import Base
from myapp.database import engine
from myapp.routers import post, user, auth
from myapp.config import Settings

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

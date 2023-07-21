from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from myapp import database, oauth2, schemas, models, utils
from sqlalchemy.orm import Session


router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(creds: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == creds.username).first()
   
    if not user:
       raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not utils.verify(creds.password, user.password):
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Invalid credentials")
    
    token = oauth2.create_access_token({"user_id":f"{user.id}"})

    return {"access_token":token, "token_type":"bearer"}
    #create a token 



    


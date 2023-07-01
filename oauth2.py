from jose import JWTError, jwt
from datetime import datetime, timedelta
from myapp import schemas, models, database
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#secret-key
#algorithm
#expiration time

SECRET_KEY = "FVFVTJUI509-59039U931NJF93EJIR904rgrg34"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict): 

    to_encode = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expiration": f"{expire_time}"})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token

def verify_token(token: str, credentials_exception):


    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id : str = payload.get("user_id")

        if id is None:
            raise credentials_exception
    
        token_data = schemas.TokenData(id=id) 

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW_Authenticate":"Bearer"})
    
    token = verify_token(token, credential_exception)

    db.query(models.User).filter(models.User.id == token.id).first()


    return verify_token(token, credential_exception)
from myapp import schemas, models, utils, database
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter

router = APIRouter(prefix="/users", tags=['Users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput)
async def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):

    #hashing the password 
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  

    return new_user


@router.get("/{id}", response_model = schemas.UserOutput)
async def get_user(id: int, db = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"user with {id} not found")

    return user
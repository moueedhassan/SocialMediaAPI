from myapp import schemas, models, utils, database, oauth2
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, Response, APIRouter

router = APIRouter(prefix="/vote", tags=["Votes"])

@router.post("", status_code=status.HTTP_201_CREATED)
def vote_post(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)): 


    if not db.query(models.Post).filter(models.Post.id == vote.post_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    vote_found = vote_query.first()

    if vote.direction == 1: 

        if vote_found is not None: 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Post with id {vote.post_id} is already voted by the user")
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "Vote successfully added!"}
    
    else: 
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Vote does not exist")
        
        vote_query.delete()
        db.commit()
        return {"message":"Vote successfully deleted!"}
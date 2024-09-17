from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, database, models
from sqlalchemy.orm import Session
from ..hashing import Hash


router = APIRouter()
get_db = database.get_db


@router.post(
    "/user",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowUser,
    tags=["Users"],
)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        email=request.email,
        name=request.name,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/user/{id}", response_model=schemas.ShowUser, tags=["Users"])
def show_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id {id} is not available"
        )
    return user

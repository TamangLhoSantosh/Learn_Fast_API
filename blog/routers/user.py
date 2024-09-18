from typing import List
from fastapi import APIRouter, Depends, status
from .. import schemas, database, oauth2
from sqlalchemy.orm import Session
from ..repository import user


router = APIRouter(prefix="/user", tags=["Users"])
get_db = database.get_db


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowUser,
)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get("/{id}", response_model=schemas.ShowUser)
def show_user(id: int, db: Session = Depends(get_db)):
    return user.show(db, id)

from fastapi import HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..hashing import Hash


def create(request: schemas.User, db: Session):
    new_user = models.User(
        email=request.email,
        name=request.name,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def show(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id {id} is not available"
        )
    return user

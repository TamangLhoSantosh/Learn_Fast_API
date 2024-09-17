from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, database, models
from sqlalchemy.orm import Session


router = APIRouter(prefix="/blog", tags=["Blogs"])
get_db = database.get_db


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=404, detail=f"Blog with id {id} is not available"
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return "done"


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=404, detail=f"Blog with id {id} is not available"
        )
    blog.update({"title": request.title, "body": request.body})
    db.commit()
    return "updated"


@router.get("/", response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get("/{id}", status_code=200, response_model=schemas.ShowBlog)
def all(id, response: Response, db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blogs:
        raise HTTPException(
            status_code=404, detail=f"Blog with id {id} is not available"
        )

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with id {id} is not available'}

    return blogs

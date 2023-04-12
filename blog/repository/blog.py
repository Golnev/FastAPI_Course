from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas


def get_all(db: Session, limit: int = 10):
    blogs = db.query(models.Blog).limit(limit).all()
    return blogs


def create(request: schemas.Blog, db: Session, current_user: schemas.TokenData):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        user_id=user.id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def destroy(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the ID {id} is not available')
    blog.delete(synchronize_session=False)
    db.commit()


def update(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the ID {id} is not available')
    blog.update(request.dict())
    db.commit()
    return blog.first()


def get_single(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the ID {id} is not available')
    return blog

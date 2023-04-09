from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from blog import schemas, models, database

router = APIRouter()


@router.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
def get_all(db: Session = Depends(database.get_db), limit: int = 10):
    blogs = db.query(models.Blog).limit(limit).all()
    return blogs


@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        user_id=1
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def destroy(id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the ID {id} is not available')
    blog.delete(synchronize_session=False)
    db.commit()


@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id: int, request: schemas.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the ID {id} is not available')
    blog.update(request.dict())
    db.commit()
    return blog.first()


@router.get('/blog/{id}', response_model=schemas.ShowBlog, tags=['blogs'])
def get_single(id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the ID {id} is not available')
    return blog

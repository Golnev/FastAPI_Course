from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from blog import schemas, database
from ..repository import blog

router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)


@router.get('', response_model=List[schemas.ShowBlog])
def get_all(db: Session = Depends(database.get_db), limit: int = 10):
    return blog.get_all(db, limit)


@router.post('', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.create(request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(database.get_db)):
    return blog.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.update(id, request, db)


@router.get('{id}', response_model=schemas.ShowBlog)
def get_single(id: int, db: Session = Depends(database.get_db)):
    return blog.get_single(id, db)

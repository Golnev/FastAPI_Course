from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from blog import schemas, database
from ..repository import user

router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('', response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return user.create_user(request, db)


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(database.get_db)):
    return user.get_user(id, db)

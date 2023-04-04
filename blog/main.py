from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from blog import models, schemas
from blog.database import engine, SessionLocal

app = FastAPI(
    title='Blog API'
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title=request.title,
        body=request.body
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the ID {id} is not available')
    blog.delete(synchronize_session=False)
    db.commit()


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the ID {id} is not available')
    blog.update(request.dict())
    db.commit()
    return blog.first()


@app.get('/blog')
def get_all(db: Session = Depends(get_db), limit: int = 10):
    blogs = db.query(models.Blog).limit(limit).all()
    return blogs


@app.get('/blog/{id}')
def get_single(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': f'Blog with the ID {id} is not available'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the ID {id} is not available')
    return blog

from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from blog import models
from blog.database import engine, SessionLocal
from blog.schemas import Blog

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
def create(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title=request.title,
        body=request.body
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}')
def get_single(pk: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == pk).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': f'Blog with the ID {pk} is not available'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the ID {pk} is not available')
    return blog

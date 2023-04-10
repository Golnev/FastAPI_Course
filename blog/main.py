from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from blog import models
from blog.database import engine
from blog.routers import blog, user

tags_metadata = [
    {
        'name': 'Blogs',
        'description': 'Operations with blogs'
    },
    {
        'name': 'Users',
        'description': 'Operations with users'
    }
]

app = FastAPI(
    title='Blog API',
    openapi_tags=tags_metadata,
    version='0.0.1',
    contact={
        'name': 'Eugene Golnev',
        'url': 'https://www.linkedin.com/in/eugene-golnev-2b2518234/',
        'email': 'eugenegolnev1993@gmail.com'
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

models.Base.metadata.create_all(bind=engine)

app.include_router(router=blog.router)
app.include_router(router=user.router)

templates = Jinja2Templates(directory='templates')


@app.get('', response_class=HTMLResponse, tags=['Main'])
def root(request: Request):
    return templates.TemplateResponse('about.html', {'request': request})

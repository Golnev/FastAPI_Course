from typing import Union, Optional

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory='templates')


@app.get('/blog')
def index(limit=10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {'data': f'{limit} published blogs'}
    else:
        return {'data': f'{limit} blogs'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'unpublished blogs'}


@app.get('/blog/{item_id}')
def show(item_id: int, q: Union[str, None] = None):
    return {'data': {'item_id': item_id, 'q': q}}


@app.get('/blog/{item_id}/comments')
def comments(item_id: int, limit: int = 10):
    return {'data': {item_id: {f'{i} from {limit}': f'{str(i)} comment' for i in range(1, (limit + 1))}}}


@app.get('/about/', response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse('about.html', {"request": request})


class Blog(BaseModel):
    title: str
    subtitle: str
    text: str
    published: Optional[bool] = False
    autor: Optional[str] = None


@app.post('/blog')
def create_blog(request: Blog):
    return {f'Blog is created with title \'\'{request.title}\'\'': request}

#
# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=9000)

from fastapi import Query
from pydantic import BaseModel


class Blog(BaseModel):
    title: str = Query(
        default=...,
        min_length=5,
        max_length=15,
        description='Blog Title'
    )
    body: str = Query(
        default=...,
        min_length=10,
        description='Blog Text'
    )

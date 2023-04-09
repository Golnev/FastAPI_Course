from typing import List

from fastapi import Query
from pydantic import BaseModel


class BlogBase(BaseModel):
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


class Blog(BlogBase):
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str = Query(
        default=...,
        description='User Name'
    )
    email: str = Query(
        default=...,
        description='User email',
        min_length=7,
    )
    password: str


class ShowUser(BaseModel):
    name: str = Query(
        default=...,
        description='User Name'
    )
    email: str = Query(
        default=...,
        description='User email',
        min_length=7,
    )
    blogs: List[Blog] = []

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
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
    creator: ShowUser

    class Config:
        orm_mode = True

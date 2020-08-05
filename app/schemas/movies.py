from typing import Optional

from pydantic import BaseModel

from app.db.node import Node


class MoviesRelation(BaseModel):
    pass


class MoviesAttribute(BaseModel):
    title: str
    tagline: Optional[str]
    released: Optional[int]


class Movies(Node):
    item_relation: Optional[MoviesRelation]
    item_attribute: MoviesAttribute

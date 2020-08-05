from typing import Optional, List

from pydantic import BaseModel

from app.db.node import Node
from app.schemas.movies import MoviesAttribute


class PersonAttribute(BaseModel):
    name: str
    born: Optional[int]


class ActedInRelation(BaseModel):
    end_node: MoviesAttribute
    roles: List[str]


class DirectedRelation(BaseModel):
    end_node: MoviesAttribute


class WroteRelation(BaseModel):
    end_node: MoviesAttribute


class ProducedRelation(BaseModel):
    end_node: MoviesAttribute


class ReviewedRelation(BaseModel):
    end_node: MoviesAttribute
    summary: str
    rating: int


class FollowsRelation(BaseModel):
    end_node: PersonAttribute


class PersonRelation(BaseModel):
    acted_in: Optional[List[ActedInRelation]]
    directed: Optional[List[DirectedRelation]]
    follows: Optional[List[FollowsRelation]]
    produced: Optional[List[ProducedRelation]]
    wrote: Optional[List[WroteRelation]]
    reviewed: Optional[List[ReviewedRelation]]


class PersonNode(Node):
    item_relation: Optional[PersonRelation]
    item_attribute: PersonAttribute

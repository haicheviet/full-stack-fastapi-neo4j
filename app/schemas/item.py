from typing import List, Optional

from pydantic import BaseModel


class GraphItem(BaseModel):
    nodes: List
    links: List


class CastItem(BaseModel):
    name: str
    job: str
    role: Optional[List[str]]


class MovieItem(BaseModel):
    title: str
    cast: List[CastItem]

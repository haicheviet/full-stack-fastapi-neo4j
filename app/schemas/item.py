from pydantic import BaseModel
from typing import List, Optional


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
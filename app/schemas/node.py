from typing import List, Optional

from pydantic import BaseModel


class RelationItem(BaseModel):
    skill: List
    position: List
    job_group: List


class RelationNode(BaseModel):
    filter: Optional[RelationItem]
    origin: Optional[RelationItem]
    language: List
    industry: List
    degree: Optional[List]

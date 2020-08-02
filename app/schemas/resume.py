from typing import List, Optional

from pydantic import BaseModel

from app.schemas.node import RelationNode


class ResumeAttributeNode(BaseModel):
    private_id: str
    create_date: int
    phone: str
    email: str
    name: str
    link: str
    public_id: str
    last_update: str

    function_id: Optional[int]
    cv_score: Optional[int]
    work_exp: Optional[int]


class ResumeNode(BaseModel):
    cv_attribute: ResumeAttributeNode
    cv_relation: RelationNode


class ResumeCreate(BaseModel):
    cv_id: str
    link: str
    last_update: str
    create_date: str

    location: Optional[str]
    js_id: Optional[str]
    city_id: Optional[str]
    position: Optional[str]
    email: Optional[str]
    username: Optional[str]
    fullname: Optional[str]
    industries: Optional[str]


class ResumeCandidate(BaseModel):
    candidate: List[ResumeAttributeNode]


class LastUpdate(BaseModel):
    last_update: str


class ResumeSkimCandidate(BaseModel):
    candidate: List[LastUpdate]

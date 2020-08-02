from typing import Optional

import ai_parser.utils.config as config
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from neo4j import BoltDriver
from starlette.requests import Request

from app.api import deps
from app.api.api_v1.misc import filter_job_group_popular, filter_duplicate_cv
from app.core.decorator import decorator_logger_info
from app.db.neo4j_jobhop.resume import Resume
from app.schemas import RelationNode, ResumeAttributeNode, ResumeNode, ResumeSkimCandidate, ResumeCandidate, \
    ResumeCreate

router = APIRouter()


@router.post("/", response_model=ResumeNode)
@decorator_logger_info
def create_resume_node(request: Request, data: ResumeCreate, driver: BoltDriver = Depends(deps.get_driver)):
    from ai_parser.processing_data.cv2content.link2text import CvQuery
    from app.db.neo4j_jobhop.update_data_neo4j import wrapper_update_cv_neo4j

    resume = Resume(driver)
    cv_query = CvQuery(cursor=None)
    data = cv_query.wrapper_get_data_cv(type_cv=config.TYPE_CV_LINK, data=data)
    data = wrapper_update_cv_neo4j(data, resume)
    return data


@router.get("/", response_model=ResumeNode)
@decorator_logger_info
def get_resume_by_id(request: Request, typeRelation: Optional[str] = "all", publicId: Optional[str] = None,
                     privateId: Optional[str] = None, driver: BoltDriver = Depends(deps.get_driver)):
    if publicId:
        q = publicId
        type_q = "publicId"
    elif privateId:
        q = privateId
        type_q = "privateId"
    else:
        raise HTTPException(status_code=404, detail="Missing params")
    type_relation = typeRelation
    resume = Resume(driver)
    if type_q == "privateId":
        json_result = resume.query_resume_by_private_id(private_id=q, type_relation=type_relation)
    else:
        json_result = resume.query_resume_by_public_id(q, type_relation=type_relation)
    return json_result


@router.get("/search/getRelation", response_model=RelationNode)
@decorator_logger_info
def get_resume_only_relation(publicId: str, request: Request, typeRelation: Optional[str] = "all",
                             driver: BoltDriver = Depends(deps.get_driver)):
    q = publicId
    type_relation = typeRelation
    resume = Resume(driver)
    json_result = resume.query_resume_relation_node(q, type_relation=type_relation)
    return json_result


@router.get("/search/getAttribute", response_model=ResumeAttributeNode)
@decorator_logger_info
def get_resume_only_attribute(publicId: str, request: Request, driver: BoltDriver = Depends(deps.get_driver)):
    q = publicId
    resume = Resume(driver)
    json_result = resume.query_resume_attribute_node(q)
    return json_result


@router.get("/byAll", response_model=ResumeCandidate, responses={200: {"model": ResumeSkimCandidate}})
@decorator_logger_info
def get_resume_by_position_and_skill(request: Request, targetSkills: Optional[str] = None,
                                     targetPosition: Optional[str] = None, typeRelation: Optional[str] = "all",
                                     targetYearExp: Optional[int] = 0, targetFreshness: Optional[str] = None,
                                     targetLevel: Optional[str] = None, driver: BoltDriver = Depends(deps.get_driver),
                                     page: Optional[int] = 1, recordPage: Optional[int] = 50):
    from ai_parser.utils.misc import normalize, convert_accented_vietnamese_text, read_json
    from ai_parser.processing_data.extract_content.extract_skill import extract_skills
    from ai_parser.processing_data.extract_content.extract_rule import extracted_job_group, extract_function

    import os

    skills_text = targetSkills
    position_text = targetPosition
    type_relation = typeRelation
    page = page
    page_record = recordPage

    if skills_text:
        skills_text = normalize(convert_accented_vietnamese_text(skills_text), nlp=request.app.nlp)
        revert_skills_dict = read_json(f"{os.getenv('DATADIR')}/revert_skills_dict.json")
        skill_dict = read_json(f"{os.getenv('DATADIR')}/skill_dict.json")
        list_skills_item = list(
            set(extract_skills(skills_text, revert_skills_dict=revert_skills_dict, skill_dict=skill_dict)))
    else:
        list_skills_item = []
    if position_text:
        position_text = normalize(convert_accented_vietnamese_text(position_text), nlp=request.app.nlp)
        job_group_dict = read_json(f"{os.getenv('DATADIR')}/revert_job_group.json")
        list_position_item = list(set(extracted_job_group(position_text, job_group_dict=job_group_dict)))
        _, function_id = extract_function(position_text)
    else:
        list_position_item = []
        function_id = -1
    if not function_id:
        function_id = -1
    list_position_item = filter_job_group_popular(list_position_item)
    if not list_skills_item and not list_position_item:
        raise HTTPException(status_code=404, detail="Position request doesn't fit with AI dictionary")

    resume = Resume(driver)
    if list_skills_item and list_position_item:
        json_result = resume.query_resume_has_skills_and_position(type_relation=type_relation,
                                                                  list_position=list_position_item,
                                                                  list_skills=list_skills_item, page=page,
                                                                  function_id=function_id, page_record=page_record)
    elif list_skills_item:
        json_result = resume.query_resume_has_list_node(type_relation=type_relation, name_relation="skill",
                                                        list_item=list_skills_item, page=page,
                                                        function_id=function_id, page_record=page_record)
    else:
        json_result = resume.query_resume_has_list_node(type_relation=type_relation, name_relation="job_group",
                                                        list_item=list_position_item, page=page,
                                                        function_id=function_id, page_record=page_record)

    if page != 0:
        json_result = filter_duplicate_cv(json_result)
    else:
        return JSONResponse(status_code=200, content=json_result)
    return json_result

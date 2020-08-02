# import os
#
# from ai_parser.utils.misc import read_json
# from fastapi import APIRouter, HTTPException
# from starlette.requests import Request
#
# from app.core.decorator import decorator_logger_info
# from app.schemas import Response
# from app.db.neo4j_jobhop.resume import Resume
#
# router = APIRouter()
#
#
# @router.get("/resumeMarketing", response_model=Response)
# @decorator_logger_info
# def cluster_resume_marketing_function(request: Request, cvId: str, driver: BoltDriver = Depends(deps.get_driver)):
#     cv_id = cvId
#     # import json
#     # mapping_job_group = init_mapping()
#     # with open(f"{os.getenv('DATADIR', 'data')}/mapping_industry.json", "w") as f:
#     #     f.write(json.dumps(mapping_job_group))
#     mapping_job_group = read_json(f"{os.getenv('DATADIR', 'data')}/mapping_industry.json")
#     resume = Resume()
#     node = resume.query_resume_by_private_id(private_id=cv_id, type_relation="filter")
#     if "cv_relation" not in node.keys():
#         from ai_parser.processing_data.cv2content.link2text import CvQuery
#         from app.db.neo4j_jobhop.update_data_neo4j import wrapper_update_cv_neo4j
#         from ai_parser.utils.database import init_cursor
#         cv_query = CvQuery(init_cursor(os.getenv('DATABASE_URL')))
#         data = cv_query.get_data_cv_id(private_id=cv_id)
#         if not data:
#             raise HTTPException(status_code=404, detail="Cv not found")
#         data["txtdata"], data["resume_language"] = cv_query.get_data_cv_from_link(data["link"])
#         _ = wrapper_update_cv_neo4j(data, resume)
#         node = resume.query_resume_by_private_id(private_id=cv_id, type_relation="filter")
#         if "cv_relation" not in node.keys():
#             raise HTTPException(status_code=404, detail="Cv not found")
#
#     list_job_group = [i[0] for i in node["cv_relation"]["filter"]["job_group"]]
#     # print(list_job_group)
#     list_skill = [i for i in node["cv_relation"]["filter"]["skill"]]
#     list_industry = []
#     if list_job_group:
#         list_job_group += [node["cv_relation"]["filter"]["job_group"][0][0]]
#         for item in list_job_group:
#             for k, v in mapping_job_group.items():
#                 if item in v:
#                     list_industry.append(k)
#                     continue
#     if not list_industry:
#         for item in list_skill:
#             for k, v in mapping_job_group.items():
#                 if item in v:
#                     list_industry.append(k)
#                     continue
#     if not list_industry:
#         raise HTTPException(status_code=200, detail="Cv content not valid")
#     industry = max(list_industry, key=list_industry.count)
#
#     return {"response": {"industry": industry}}

from fastapi import APIRouter, Depends
from neo4j.work.simple import Session
from starlette.requests import Request

from app.api import deps
from app.core.decorator import decorator_logger_info
from app.schemas import GraphItem

router = APIRouter()


@router.get("/graph", response_model=GraphItem)
@decorator_logger_info
def get_graph(request: Request, limit: int = 100, session: Session = Depends(deps.get_db)):
    results = session.run("MATCH (m:Movie)<-[:ACTED_IN]-(a:Person) "
             "RETURN m.title as movie, collect(a.name) as cast "
             "LIMIT $limit", {"limit": limit})
    nodes = []
    rels = []
    i = 0
    for record in results:
        nodes.append({"title": record["movie"], "label": "movie"})
        target = i
        i += 1
        for name in record['cast']:
            actor = {"title": name, "label": "actor"}
            try:
                source = nodes.index(actor)
            except ValueError:
                nodes.append(actor)
                source = i
                i += 1
            rels.append({"source": source, "target": target})

    return {"nodes": nodes, "links": rels}

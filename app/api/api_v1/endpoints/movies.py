from typing import List, Any

from fastapi import APIRouter, Depends, Path
from neo4j.work.simple import Session
from starlette.requests import Request

from app.api import deps
from app.core.decorator import decorator_logger_info
from app.db.node import Node
from app.schemas import MoviesAttribute, MovieItem

router = APIRouter()


@router.get("/search", response_model=List[MoviesAttribute])
@decorator_logger_info
def get_movie_search(title: str, request: Request, session: Session = Depends(deps.get_db)) -> Any:
    results = session.run("MATCH (movie:Movie) "
                          "WHERE movie.title =~ $title "
                          "RETURN movie", {"title": "(?i).*" + title + ".*"})
    results = [Node.serialize_node(i["movie"]) for i in results]
    return results


def serialize_cast(cast):
    return {
        'name': cast[0],
        'job': cast[1],
        'role': cast[2]
    }


@router.get("/{title}", response_model=MovieItem)
@decorator_logger_info
def get_movie(request: Request, title: str = Path(..., title="Title of movies"),
              session: Session = Depends(deps.get_db)):
    results = session.run("MATCH (movie:Movie {title:$title}) "
                          "OPTIONAL MATCH (movie)<-[r]-(person:Person) "
                          "RETURN movie.title as title,"
                          "collect([person.name, "
                          "         head(split(toLower(type(r)), '_')), r.roles]) as cast "
                          "LIMIT 1", {"title": title})

    result = results.single()
    result = Node.serialize_node(result)
    result["cast"] = [serialize_cast(i) for i in result["cast"]]

    return result

from fastapi import APIRouter
from fastapi import Depends

from app.api.api_v1.endpoints import items, movies
from app.api.deps import get_current_username

api_router = APIRouter()
# api_router.include_router(login.router, tags=["login"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, tags=["items"],
                          dependencies=[Depends(get_current_username)])
api_router.include_router(movies.router, prefix="/movies", tags=["movies"],
                          dependencies=[Depends(get_current_username)])
# api_router.include_router(marketing.router, tags=["marketing_api"],
#                           dependencies=[Depends(get_current_username)])


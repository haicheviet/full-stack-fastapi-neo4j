from typing import Any

from fastapi import APIRouter

from app import schemas
from app.core.celery_app import celery_app

router = APIRouter()


@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(msg: schemas.Msg) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}

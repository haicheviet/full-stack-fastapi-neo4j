from typing import Dict

from fastapi.testclient import TestClient
from requests.auth import _basic_auth_str

from app.core.config import settings


def get_superuser_headers(client: TestClient) -> Dict[str, str]:
    headers = {"Authorization": _basic_auth_str(settings.FIRST_SUPERUSER, settings.FIRST_SUPERUSER_PASSWORD)}
    return headers

from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


def test_graph_item(
        client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/graph", headers=superuser_token_headers)
    graph_item = r.json()
    assert graph_item
    assert graph_item["nodes"]
    assert {"title": "The Matrix", "label": "movie"} in graph_item["nodes"]

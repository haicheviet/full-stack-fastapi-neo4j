from urllib.parse import urlparse

from neo4j import GraphDatabase

from app.core.config import settings

url = f"{settings.NEO4J_SCHEME}://{settings.NEO4J_SERVER}:7687"
driver = GraphDatabase.driver(url, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
SessionLocal = driver.session

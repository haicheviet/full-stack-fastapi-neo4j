from urllib.parse import urlparse

from neo4j import GraphDatabase
from app.core.config import settings

def get_driver(database_url):
    database_url = urlparse(database_url)
    url = f"{database_url.scheme}://{database_url.hostname}:{database_url.port}"
    driver = GraphDatabase.driver(url, auth=(database_url.username, database_url.password))
    return driver

driver = get_driver(settings.NEO4J_DATABASE_URL)
SessionLocal = driver.session
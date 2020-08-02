from neo4j.work.simple import Session
import logging
from glob import glob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(session: Session) -> None:
    result = session.run("MATCH (m:Movie) return m.movies")
    temp = None
    for record in result:
        temp = record
    if not temp:
        logging.info("Initalize database movie")
        for file_name in glob("app/db/migrations/*.cypher"):
            logging.info(f"Attempting to run cypher: {file_name}")
            with open(file_name, "r") as f:
                content = f.read()
            session.run(content)
        for file_name in glob("app/db/migrations/index/*.cypher"):
            logging.info(f"Attempting to run cypher: {file_name}")
            with open(file_name, "r") as f:
                content = f.read()
            session.run(content)
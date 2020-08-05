import traceback

from app.core.celery_app import celery_app
from app.db.session import SessionLocal


@celery_app.task()
def back_up_scrip():
    logger = back_up_scrip.get_logger()
    session = SessionLocal()
    result = session.run("""
            CALL apoc.export.cypher.all("import/all.cypher", {
            format: "cypher-shell",
            useOptimizations: {type: "UNWIND_BATCH", unwindBatchSize: 20}
            })
            YIELD file, batches, source, format, nodes, relationships, properties, time, rows, batchSize
            RETURN file, batches, source, format, nodes, relationships, properties, time, rows, batchSize;
             """)
    for record in result:
        try:
            logger.info(f"{record['file']}")
        except:
            logger.info(f"{traceback.format_exc()}")
        finally:
            session.close()
        break

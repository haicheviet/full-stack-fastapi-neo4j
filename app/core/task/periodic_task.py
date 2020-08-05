import datetime
import traceback

import celery

from app.db.session import SessionLocal


@celery.task()
def back_up_scrip():
    logger = back_up_scrip.get_logger()
    session = SessionLocal()
    ts_now = int(datetime.datetime.now().timestamp())
    result = session.run("""
            CALL apoc.export.cypher.all("import/backup_%s.cypher", {
            format: "cypher-shell",
            useOptimizations: {type: "UNWIND_BATCH", unwindBatchSize: 20}
            })
            YIELD file, batches, source, format, nodes, relationships, properties, time, rows, batchSize
            RETURN file, batches, source, format, nodes, relationships, properties, time, rows, batchSize;
             """ % ts_now)
    for record in result:
        try:
            logger.info(f"{record['file']}")
        except:
            logger.info(f"{traceback.format_exc()}")
        finally:
            session.close()
        break

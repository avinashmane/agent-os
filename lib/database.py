from agno.db.postgres import PostgresDb
from  loguru import logger
import os

# Database connection
db_url = os.getenv("DB_URL")
id = "default"
# session_table_name='sessions'

# Create Postgres-backed memory store
def get_db(id=id, **kw
           ):   
     
#      session_table=None,
       #     memory_table=None,
       #     knowledge_table=None
    logger.info(f"Database URL: {db_url}")
    return PostgresDb(id=id,
                      db_url=db_url, 
                      **kw)

# db = get_db()
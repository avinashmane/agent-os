from agno.db.postgres import PostgresDb

# Database connection
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
id = "default"
# session_table_name='sessions'

# Create Postgres-backed memory store
def get_db(id=id, **kw
           ):   
#      session_table=None,
       #     memory_table=None,
       #     knowledge_table=None
    return PostgresDb(id=id,
                      db_url=db_url, 
                      **kw)

# db = get_db()
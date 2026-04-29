import asyncio
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from agno.db.migrations.manager import MigrationManager

from agno.db.postgres import AsyncPostgresDb
from lib import get_db
db = get_db()

async def run_migrations():
    # Migrate all tables to latest version
    await MigrationManager(db).up()
    
    # # Migrate specific table to specific version
    # await MigrationManager(db).up(
    #     target_version="2.3.0",
    #     table_type="memory"
    # )
    
    # # Force migration
    # await MigrationManager(db).up(
    #     table_type="session",
    #     force=True
    # )

if __name__ == "__main__":
    asyncio.run(run_migrations())


from .database import get_db
from .knowledge import get_vector_db,get_knowledge_base
from .model import model, get_model


import os
def env(key,default=None):
    return os.environ.get(key,default)

from  loguru import logger
logger.info(f"Environment: {os.getenv('APP_ROOT')}")

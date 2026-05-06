import os



from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

from .loggin import logger
logger.info("loading env")

from .database import get_db
from .knowledge import get_vector_db,get_knowledge_base
from .model import model, get_model


def env(key,default=None):
    return os.environ.get(key,default)



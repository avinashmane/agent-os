

from .database import get_db
from .knowledge import get_vector_db
from .model import model, get_model


import os
def env(key,default=None):
    return os.environ.get(key,default)
from  loguru import logger
import os
# Configure logging
logger.add("logger.log", rotation="1 MB", level="INFO")

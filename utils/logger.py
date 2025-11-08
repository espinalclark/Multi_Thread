import logging
from utils.config import DOWNLOADS_PATH
import os

# Crear carpeta de logs si no existe
LOG_DIR = os.path.join(DOWNLOADS_PATH, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "system.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def log_info(message: str):
    logging.info(message)

def log_error(message: str):
    logging.error(message)

def log_warning(message: str):
    logging.warning(message)


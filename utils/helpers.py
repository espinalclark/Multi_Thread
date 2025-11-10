import os
from utils.config import DOWNLOADS_PATH, TEMP_PATH

def ensure_directories_exist(username: str):
    """
    Asegura que existan las carpetas necesarias para cada usuario
    """
    user_path = os.path.join(DOWNLOADS_PATH, username)
    os.makedirs(user_path, exist_ok=True)
    os.makedirs(TEMP_PATH, exist_ok=True)
    return user_path, TEMP_PATH

def format_bytes(size):
    """
    Convierte bytes a una representación legible (KB, MB, GB)
    """
    for unit in ['B','KB','MB','GB','TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


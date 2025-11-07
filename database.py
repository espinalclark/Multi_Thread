import mysql.connector
from mysql.connector import Error
from utils.config import DATABASE_CONFIG

def get_connection():
    """
    Conecta con la base de datos MariaDB y devuelve la conexión
    """
    try:
        conn = mysql.connector.connect(
            host=DATABASE_CONFIG["host"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"],
            database=DATABASE_CONFIG["database"],
            port=DATABASE_CONFIG["port"]
        )
        return conn
    except Error as e:
        print(f"Error de conexión: {e}")
        return None


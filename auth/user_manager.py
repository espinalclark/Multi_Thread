# auth/user_manager.py
from database import get_connection
from auth.password_utils import hash_password, check_password

def create_user(username: str, email: str, password: str, role: str = "user") -> bool:
    """Crea un usuario en la base de datos."""
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        hashed = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
            (username, email, hashed, role)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error creando usuario: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_user_by_username(username: str):
    """Obtiene datos de un usuario por su nombre de usuario."""
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error obteniendo usuario: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


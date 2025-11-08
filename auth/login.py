# auth/login.py
from auth.user_manager import get_user_by_username
from auth.password_utils import check_password
import bcrypt

class LoginApp:
    def __init__(self):
        pass  # No necesitamos la ventana aquí

    def login_user(self, username, password):
        user_data = get_user_by_username(username)
        if not user_data:
            return None, "Usuario no encontrado ❌"

        if check_password(password, user_data[3]):
            return user_data, None
        else:
            return None, "Contraseña incorrecta ❌"


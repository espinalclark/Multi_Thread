import bcrypt
import re

def hash_password(password: str) -> str:
    """Hashea una contraseña en texto plano."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    """Verifica si la contraseña coincide con el hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def validate_dni(dni: str) -> bool:
    """Valida que el DNI tenga exactamente 8 dígitos."""
    return bool(re.fullmatch(r"\d{8}", dni))

def validate_password(password: str) -> bool:
    """Valida que la contraseña sea segura: mínimo 8, mayúsculas, minúsculas, números y símbolos."""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>#\$]", password):
        return False
    return True


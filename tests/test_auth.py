import unittest
from auth.user_manager import create_user, get_user
from auth.password_utils import hash_password, verify_password

class TestAuth(unittest.TestCase):
    def setUp(self):
        # Datos de prueba
        self.username = "neider"
        self.email = "neider@example.com"
        self.password = "neiderdelacruz"

    def test_password_hashing(self):
        hashed = hash_password(self.password)
        self.assertTrue(verify_password(self.password, hashed))

    def test_create_and_get_user(self):
        # Crea usuario de prueba (en memoria o mock)
        create_user(self.username, self.email, self.password, role='user')
        user = get_user(self.username)
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], self.username)

if __name__ == "__main__":
    unittest.main()


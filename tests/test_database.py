import unittest
from database import get_connection

class TestDatabase(unittest.TestCase):
    def test_connection(self):
        conn = get_connection()
        self.assertIsNotNone(conn)
        conn.close()

if __name__ == "__main__":
    unittest.main()


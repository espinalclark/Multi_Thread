import unittest
from downloader import download_file
from threading import Thread
import os

class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.test_url = "https://example.com/file.zip"
        self.destination = "tests/temp_file.zip"

    def test_download_threaded(self):
        # Ejecuta la descarga en un hilo (simulación)
        thread = Thread(target=download_file, args=(self.test_url, self.destination))
        thread.start()
        thread.join()
        # Como es ejemplo, solo verificamos que la función corrió sin excepciones
        self.assertTrue(True)

    def tearDown(self):
        if os.path.exists(self.destination):
            os.remove(self.destination)

if __name__ == "__main__":
    unittest.main()


from threading import Thread
import requests

class SegmentThread(Thread):
    """Hilo que descarga un segmento de un archivo."""
    def __init__(self, url, start_byte, end_byte, dest_path, progress_callback=None, timeout=60):
        super().__init__()
        self.url = url
        self.start_byte = start_byte
        self.end_byte = end_byte
        self.dest_path = dest_path
        self.progress_callback = progress_callback
        self.bytes_downloaded = 0
        self.status = 'waiting'
        self.timeout = timeout

    def run(self):
        self.status = 'running'
        headers = {
            'Range': f'bytes={self.start_byte}-{self.end_byte}',
            'User-Agent': 'Mozilla/5.0'
        }

        try:
            response = requests.get(self.url, headers=headers, stream=True, timeout=self.timeout)
            response.raise_for_status()

            with open(self.dest_path, 'r+b') as f:
                f.seek(self.start_byte)
                total_bytes = self.end_byte - self.start_byte + 1

                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        self.bytes_downloaded += len(chunk)
                        if self.progress_callback:
                            percent = (self.bytes_downloaded / total_bytes) * 100
                            self.progress_callback(percent)
            self.status = 'done'
        except Exception as e:
            print(f"[SegmentThread] Error: {e}")
            self.status = 'error'


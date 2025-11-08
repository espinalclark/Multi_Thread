import os
import math
import requests
from threads.segment_thread import SegmentThread

try:
    from yt_dlp import YoutubeDL
    YTDLP_AVAILABLE = True
except ImportError:
    YTDLP_AVAILABLE = False

def start_multithread_download(url, dest_dir, num_threads=1, filename=None, progress_callback=None, timeout=60):
    os.makedirs(dest_dir, exist_ok=True)

    if not filename:
        filename = url.split("/")[-1].split("?")[0]
    file_path = os.path.join(dest_dir, filename)

    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.head(url, headers=headers, allow_redirects=True, timeout=timeout)
    total_size = int(response.headers.get('Content-Length', 0))
    if total_size == 0:
        raise ValueError("Content-Length desconocido, no se puede usar multihilo")

    with open(file_path, "wb") as f:
        f.truncate(total_size)

    segment_size = math.ceil(total_size / num_threads)
    threads = []
    segment_progress = [0] * num_threads

    def make_callback(index):
        def callback(percent):
            segment_progress[index] = percent
            if progress_callback:
                progress_callback(sum(segment_progress) / num_threads)
        return callback

    for i in range(num_threads):
        start_byte = i * segment_size
        end_byte = min(start_byte + segment_size - 1, total_size - 1)
        t = SegmentThread(url, start_byte, end_byte, file_path, make_callback(i), timeout=timeout)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return file_path

def download_with_yt_dlp(url, dest_dir, progress_callback=None, filename=None):
    os.makedirs(dest_dir, exist_ok=True)
    outtmpl = filename or '%(title)s.%(ext)s'
    ydl_opts = {
        'outtmpl': os.path.join(dest_dir, outtmpl),
        'noplaylist': True,
        'progress_hooks': []
    }

    if progress_callback:
        def hook(d):
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                if total:
                    percent = downloaded / total * 100
                    progress_callback(percent)
        ydl_opts['progress_hooks'].append(hook)

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info = ydl.extract_info(url, download=False)
        final_name = ydl.prepare_filename(info)
        return final_name

def start_download(url, dest_dir, num_threads=4, filename=None, progress_callback=None, timeout=60):
    try:
        return start_multithread_download(url, dest_dir, num_threads, filename, progress_callback, timeout)
    except Exception as e:
        if YTDLP_AVAILABLE:
            print(f"Multihilo falló: {e}. Usando yt-dlp como fallback...")
            return download_with_yt_dlp(url, dest_dir, progress_callback, filename)
        else:
            raise RuntimeError(f"No se pudo descargar el archivo y yt-dlp no está disponible: {e}")


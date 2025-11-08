import os
import math
import requests
from threads.segment_thread import SegmentThread

try:
    from yt_dlp import YoutubeDL
    YTDLP_AVAILABLE = True
except ImportError:
    YTDLP_AVAILABLE = False

def start_multithread_download(url, dest_dir, num_threads=1, filename=None, progress_callback=None):
    """
    Descarga un archivo usando múltiples hilos.
    """
    os.makedirs(dest_dir, exist_ok=True)

    if not filename:
        filename = url.split("/")[-1].split("?")[0]
    file_path = os.path.join(dest_dir, filename)

    # Solicitar headers para obtener tamaño del archivo
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.head(url, headers=headers, allow_redirects=True, timeout=10)
    total_size = int(response.headers.get('Content-Length', 0))
    if total_size == 0:
        raise ValueError("Content-Length desconocido, no se puede usar multihilo")

    # Crear archivo vacío
    with open(file_path, "wb") as f:
        f.truncate(total_size)

    # Calcular rangos por segmento
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
        t = SegmentThread(url, start_byte, end_byte, file_path, make_callback(i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return file_path

def download_with_yt_dlp(url, dest_dir, progress_callback=None, filename=None):
    """
    Descarga cualquier video o enlace streaming usando yt-dlp.
    """
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

def start_download(url, dest_dir, num_threads=4, filename=None, progress_callback=None):
    """
    Función principal: intenta multihilo primero y luego yt-dlp como fallback.
    """
    try:
        return start_multithread_download(url, dest_dir, num_threads, filename, progress_callback)
    except Exception as e:
        if YTDLP_AVAILABLE:
            print(f"Multihilo falló: {e}. Usando yt-dlp como fallback...")
            return download_with_yt_dlp(url, dest_dir, progress_callback, filename)
        else:
            raise RuntimeError(f"No se pudo descargar el archivo y yt-dlp no está disponible: {e}")

if __name__ == '__main__':
    import argparse
    import logging

    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

    parser = argparse.ArgumentParser(description="Gestor de descargas universal")
    parser.add_argument('url', help='URL a descargar')
    parser.add_argument('-o', '--out', default='downloads', help='Directorio de salida')
    parser.add_argument('-n', '--name', help='Nombre de archivo de salida (opcional)')
    args = parser.parse_args()

    def print_progress(p):
        print(f"Progreso: {p:.2f}%")

    path = start_download(args.url, args.out, filename=args.name, progress_callback=print_progress)
    print("Archivo guardado en:", path)


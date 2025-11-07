import os
import math
import requests
from threads.segment_thread import SegmentThread

def start_download(url, dest_dir, num_threads=4, filename=None, progress_callback=None):
    """
    Descarga un archivo usando múltiples hilos.
    """
    # Crear directorio si no existe
    os.makedirs(dest_dir, exist_ok=True)

    # Obtener nombre del archivo desde URL si no se especifica
    if not filename:
        filename = url.split("/")[-1].split("?")[0]
    file_path = os.path.join(dest_dir, filename)

    # Solicitar headers para obtener tamaño del archivo
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }
    response = requests.head(url, headers=headers)
    total_size = int(response.headers.get('Content-Length', 0))

    # Crear archivo vacío con tamaño correcto
    with open(file_path, "wb") as f:
        f.truncate(total_size)

    # Calcular rangos por segmento
    segment_size = math.ceil(total_size / num_threads)
    threads = []
    segment_progress = [0] * num_threads

    # Callback para actualizar progreso total
    def make_callback(index):
        def callback(percent):
            segment_progress[index] = percent
            if progress_callback:
                # Suma de todos los segmentos dividido entre cantidad de segmentos
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


import tkinter as tk
from tkinter import ttk, messagebox
from downloader import start_download
import threading
import os

class DashboardApp(tk.Tk):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.title(f"Multi-Thread Downloader - Bienvenido {user_data[1]}")
        self.geometry("650x450")
        self.resizable(False, False)
        self.configure(bg="#1E1E1E")

        self.create_styles()
        self.create_widgets()

    def create_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TLabel", background="#1E1E1E", foreground="#FFFFFF", font=("Segoe UI", 11))
        style.configure("TEntry", padding=8, font=("Segoe UI", 11),
                        fieldbackground="#2C2C2C", foreground="#FFFFFF", relief="flat")
        style.configure("TButton", font=("Segoe UI Semibold", 11), padding=10,
                        background="#0078D7", foreground="#FFFFFF", borderwidth=0)
        style.map("TButton", background=[("active", "#005A9E")])

    def create_widgets(self):
        ttk.Label(self, text="Multi-Thread Downloader", font=("Segoe UI Semibold", 18)).pack(pady=(20, 10))

        ttk.Label(self, text="URL del archivo:").pack(anchor="w", padx=30)
        self.url_entry = ttk.Entry(self, width=70)
        self.url_entry.pack(pady=(0, 10))

        ttk.Label(self, text="Nombre de archivo (opcional):").pack(anchor="w", padx=30)
        self.filename_entry = ttk.Entry(self, width=70)
        self.filename_entry.pack(pady=(0, 10))

        ttk.Label(self, text="Número de hilos:").pack(anchor="w", padx=30)
        self.threads_entry = ttk.Entry(self, width=10)
        self.threads_entry.insert(0, "4")
        self.threads_entry.pack(pady=(0, 10))

        self.progress = ttk.Progressbar(self, orient="horizontal", length=550, mode="determinate")
        self.progress.pack(pady=(20, 10))

        ttk.Button(self, text="Iniciar Descarga", command=self.start_download_thread).pack(pady=(10, 5))

        self.history_text = tk.Text(self, height=8, width=80, bg="#2C2C2C", fg="#FFFFFF")
        self.history_text.pack(pady=(10, 10))
        self.history_text.insert(tk.END, "Historial de descargas:\n")

    def start_download_thread(self):
        url = self.url_entry.get().strip()
        filename = self.filename_entry.get().strip() or None
        try:
            num_threads = int(self.threads_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Número de hilos inválido")
            return

        if not url:
            messagebox.showerror("Error", "Ingresa la URL del archivo")
            return

        self.progress["value"] = 0
        threading.Thread(target=self.download_file, args=(url, filename, num_threads)).start()

    def download_file(self, url, filename, num_threads):
        try:
            def progress_callback(percent):
                self.progress["value"] = percent

            dest_dir = os.path.join(os.getcwd(), "downloads")
            file_path = start_download(url, dest_dir, num_threads, filename, progress_callback)
            self.history_text.insert(tk.END, f"✅ {file_path}\n")
            messagebox.showinfo("Descarga completada", f"Archivo descargado en:\n{file_path}")
        except Exception as e:
            self.history_text.insert(tk.END, f"❌ Error: {e}\n")
            messagebox.showerror("Error", f"No se pudo descargar el archivo:\n{e}")



import tkinter as tk
from tkinter import ttk, messagebox
from downloader import start_download
import threading
import time
import os

# Botón redondeado
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text="", command=None, radius=20, width=150, height=40, bg="#0078D7", fg="white", font=("Segoe UI Semibold", 14)):
        super().__init__(parent, borderwidth=0, highlightthickness=0, bg=parent["bg"], width=width, height=height)
        self.command = command
        self.radius = radius
        self.bg = bg
        self.fg = fg
        self.font = font
        self.width = width
        self.height = height
        self.text = text
        self.draw_button()
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", lambda e: self.itemconfig("rect", fill="#005A9E"))
        self.bind("<Leave>", lambda e: self.itemconfig("rect", fill=self.bg))

    def draw_button(self):
        r = self.radius
        w = self.width
        h = self.height
        self.create_rectangle(r, 0, w-r, h, fill=self.bg, outline=self.bg, tags="rect")
        self.create_oval(0, 0, r*2, h, fill=self.bg, outline=self.bg, tags="rect")
        self.create_oval(w-2*r, 0, w, h, fill=self.bg, outline=self.bg, tags="rect")
        self.create_text(w//2, h//2, text=self.text, fill=self.fg, font=self.font)

    def on_click(self, event):
        if self.command:
            self.command()


class DashboardApp(tk.Tk):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.title(f"Multi Thread Download - {user_data.get('name', '')}")
        self.geometry("900x550")
        self.resizable(False, False)
        self.configure(bg="#1a1a1a")
        self.create_widgets()

    def create_widgets(self):
        # Panel izquierdo: historial pequeño
        self.left_panel = tk.Frame(self, bg="#2C2C2C", width=200)
        self.left_panel.pack(side="left", fill="y")

        tk.Label(self.left_panel, text="Historial", bg="#2C2C2C", fg="white",
                 font=("Segoe UI Semibold", 14)).pack(pady=10)
        self.history_text = tk.Text(self.left_panel, bg="#1E1E1E", fg="white",
                                    font=("Segoe UI", 11), width=25, height=30, bd=0)
        self.history_text.pack(padx=10, pady=5, fill="y", expand=True)
        self.history_text.insert(tk.END, "Historial de descargas:\n")
        self.history_text.config(state="disabled")

        # Panel derecho: descargas
        self.right_panel = tk.Frame(self, bg="#1a1a1a")
        self.right_panel.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Título Multi Thread
        tk.Label(self.right_panel, text="Multi Thread", bg="#1a1a1a", fg="white", font=("Segoe UI Semibold", 22)).pack(pady=(0,5))
        # Nombre del usuario debajo
        tk.Label(self.right_panel, text=f"{self.user_data.get('name','')}", bg="#1a1a1a", fg="white", font=("Segoe UI Semibold", 18)).pack(pady=(0,15))

        # URL
        tk.Label(self.right_panel, text="URL del archivo:", bg="#1a1a1a", fg="white", font=("Segoe UI", 12)).pack(anchor="w")
        self.url_entry = tk.Entry(self.right_panel, bg="#2C2C2C", fg="white", insertbackground="white", font=("Segoe UI", 12), bd=0)
        self.url_entry.pack(fill="x", pady=(0,10))

        # Nombre del archivo
        tk.Label(self.right_panel, text="Nombre del archivo (opcional):", bg="#1a1a1a", fg="white", font=("Segoe UI", 12)).pack(anchor="w")
        self.filename_entry = tk.Entry(self.right_panel, bg="#2C2C2C", fg="white", insertbackground="white", font=("Segoe UI", 12), bd=0)
        self.filename_entry.pack(fill="x", pady=(0,10))

        # Número de hilos
        tk.Label(self.right_panel, text="Número de hilos:", bg="#1a1a1a", fg="white", font=("Segoe UI", 12)).pack(anchor="w")
        self.threads_entry = tk.Entry(self.right_panel, bg="#2C2C2C", fg="white", insertbackground="white", font=("Segoe UI", 12), bd=0)
        self.threads_entry.insert(0, "4")
        self.threads_entry.pack(fill="x", pady=(0,10))

        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.right_panel, orient="horizontal", length=500, mode="determinate", variable=self.progress_var)
        self.progress_bar.pack(pady=(20,5))

        # Texto progreso
        self.progress_label = tk.Label(self.right_panel, text="0% | 0 KB/s", bg="#1a1a1a", fg="white", font=("Segoe UI", 11))
        self.progress_label.pack()

        # Botón iniciar descarga
        self.download_btn = RoundedButton(self.right_panel, text="Iniciar Descarga", command=self.start_download_thread, width=200, height=45, radius=20)
        self.download_btn.pack(pady=20)

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

        threading.Thread(target=self.download_file, args=(url, filename, num_threads), daemon=True).start()

    def download_file(self, url, filename, num_threads):
        dest_dir = os.path.join(os.getcwd(), "downloads")
        start_time = time.time()
        last_bytes = [0]

        def progress_callback(percent, downloaded_bytes=None):
            elapsed = max(time.time() - start_time, 0.001)
            speed = (downloaded_bytes or 0) / elapsed
            text = f"{percent:.1f}% | {self.human_readable(speed)}/s"
            # Actualizar desde el hilo principal
            self.progress_bar.after(0, lambda: self.progress_var.set(percent))
            self.progress_label.after(0, lambda: self.progress_label.config(text=text))

        try:
            file_path = start_download(url, dest_dir, num_threads, filename,
                                       lambda p: progress_callback(p, last_bytes[0]))
            # Actualizar historial
            self.history_text.after(0, lambda: self.append_history(f" {file_path}"))
            messagebox.showinfo("Descarga completada", f"Archivo descargado en:\n{file_path}")
        except Exception as e:
            self.history_text.after(0, lambda: self.append_history(f" Error: {e}"))
            messagebox.showerror("Error", f"No se pudo descargar el archivo:\n{e}")

    def append_history(self, text):
        self.history_text.config(state="normal")
        self.history_text.insert(tk.END, f"{text}\n")
        self.history_text.see(tk.END)
        self.history_text.config(state="disabled")

    @staticmethod
    def human_readable(bytes_size):
        for unit in ["B","KB","MB","GB"]:
            if bytes_size < 1024:
                return f"{bytes_size:.1f}{unit}"
            bytes_size /= 1024
        return f"{bytes_size:.1f}TB"


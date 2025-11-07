# ui/login_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from auth.login import LoginApp as AuthLoginApp
from ui.dashboard import DashboardApp  # Importa tu dashboard

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login - MultiThread Manager")
        self.geometry("400x500")
        self.resizable(False, False)
        self.configure(bg="#1E1E1E")
        self.center_window()
        self.create_styles()
        self.create_widgets()

    def center_window(self):
        w, h = 400, 500
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

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
        ttk.Label(self, text="Iniciar Sesión", font=("Segoe UI Semibold", 20)).pack(pady=(60, 10))
        ttk.Label(self, text="Usuario:").pack(anchor="w", padx=60)
        self.username = ttk.Entry(self, width=30)
        self.username.pack(pady=(0, 15))

        ttk.Label(self, text="Contraseña:").pack(anchor="w", padx=60)
        self.password = ttk.Entry(self, width=30, show="•")
        self.password.pack(pady=(0, 25))

        ttk.Button(self, text="Ingresar", command=self.login).pack(pady=10, ipadx=10)

    def login(self):
        user = self.username.get().strip()
        pwd = self.password.get().strip()

        if not user or not pwd:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos")
            return

        # Usar AuthLoginApp para autenticar
        auth = AuthLoginApp()
        user_data, error = auth.login_user(user, pwd)

        if error:
            messagebox.showerror("Error", error)
            return

        # Login exitoso: cerrar login y abrir dashboard
        self.destroy()
        dashboard = DashboardApp(user_data)  # <-- pasamos user_data
        dashboard.mainloop()


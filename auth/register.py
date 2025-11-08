# auth/register.py
import tkinter as tk
from tkinter import ttk, messagebox
from auth.user_manager import create_user

class RegisterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registro - MultiThread Manager")
        self.geometry("400x500")
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
        ttk.Label(self, text="Registro de Usuario", font=("Segoe UI Semibold", 20)).pack(pady=(60, 10))

        ttk.Label(self, text="Usuario:").pack(anchor="w", padx=60)
        self.username = ttk.Entry(self, width=30)
        self.username.pack(pady=(0, 15))

        ttk.Label(self, text="Email:").pack(anchor="w", padx=60)
        self.email = ttk.Entry(self, width=30)
        self.email.pack(pady=(0, 15))

        ttk.Label(self, text="Contraseña:").pack(anchor="w", padx=60)
        self.password = ttk.Entry(self, width=30, show="•")
        self.password.pack(pady=(0, 15))

        ttk.Button(self, text="Registrar", command=self.register_user).pack(pady=20, ipadx=10)

    def register_user(self):
        user = self.username.get().strip()
        email = self.email.get().strip()
        password = self.password.get().strip()

        if not user or not email or not password:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
            return

        if create_user(user, email, password):
            messagebox.showinfo("Éxito", "Usuario creado correctamente ✅")
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo crear el usuario ❌")

if __name__ == "__main__":
    app = RegisterApp()
    app.mainloop()


import tkinter as tk
from tkinter import messagebox
from auth.user_manager import create_user
from auth.password_utils import validate_dni, validate_password

class RegisterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registro - MultiThread Manager")
        self.geometry("400x500")
        self.resizable(False, False)
        self.configure(bg="#1E1E1E")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Registro de Usuario", font=("Segoe UI Semibold", 20), bg="#1E1E1E", fg="white").pack(pady=(60, 20))

        tk.Label(self, text="DNI (8 dígitos):", bg="#1E1E1E", fg="white").pack(anchor="w", padx=50)
        self.dni_entry = tk.Entry(self, width=25)
        self.dni_entry.pack(pady=(0, 15))

        tk.Label(self, text="Contraseña:", bg="#1E1E1E", fg="white").pack(anchor="w", padx=50)
        self.pass_entry = tk.Entry(self, width=25, show="•")
        self.pass_entry.pack(pady=(0, 15))

        tk.Button(self, text="Registrar", command=self.register_user, bg="#0078D7", fg="white").pack(pady=20, ipadx=10)

    def register_user(self):
        dni = self.dni_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not dni or not password:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos")
            return

        if not validate_dni(dni):
            messagebox.showerror("Error", "DNI inválido (debe tener 8 dígitos)")
            return

        if not validate_password(password):
            messagebox.showerror("Error", "Contraseña insegura. Debe tener mínimo 8 caracteres, mayúsculas, minúsculas, números y símbolos")
            return

        if create_user(dni, password):
            messagebox.showinfo("Éxito", "Usuario creado correctamente")
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo crear el usuario")

if __name__ == "__main__":
    app = RegisterApp()
    app.mainloop()


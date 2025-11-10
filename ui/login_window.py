import tkinter as tk
from tkinter import messagebox
from auth.login import LoginApp as AuthLoginApp
from ui.dashboard import DashboardApp
from auth.register import RegisterApp

class RoundedButton(tk.Canvas):
    """Botón redondeado para Tkinter"""
    def __init__(self, parent, text="", command=None, radius=20, width=180, height=45, bg="#0078D7", fg="white", font=("Segoe UI Semibold", 14)):
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

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi_Thread")
        self.geometry("400x500")
        self.configure(bg="#1a1a1a")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self, bg="#1a1a1a")
        frame.place(relx=0.5, rely=0.5, anchor="c")

        # Título
        tk.Label(frame, text="Multi_Thread", fg="white", bg="#1a1a1a",
                 font=("Segoe UI Semibold", 24)).pack(pady=(0,40))

        # --- Usuario ---
        user_frame = tk.Frame(frame, bg="#1a1a1a")
        user_frame.pack(fill="x", pady=(0,20))
        tk.Label(user_frame, text="✉️", bg="#1a1a1a", fg="white", font=("Segoe UI", 12)).pack(side="left", padx=(0,5))
        self.user_entry = tk.Entry(user_frame, fg="white", bg="#1a1a1a", insertbackground="white",
                                   font=("Segoe UI", 12), bd=0, highlightthickness=0)
        self.user_entry.pack(side="left", fill="x", expand=True)
        tk.Frame(frame, bg="white", height=1).pack(fill="x", pady=(0,15))

        # --- Contraseña ---
        pass_frame = tk.Frame(frame, bg="#1a1a1a")
        pass_frame.pack(fill="x", pady=(0,20))
        tk.Label(pass_frame, text="🔒", bg="#1a1a1a", fg="white", font=("Segoe UI", 12)).pack(side="left", padx=(0,5))
        self.pass_entry = tk.Entry(pass_frame, fg="white", bg="#1a1a1a", insertbackground="white",
                                   font=("Segoe UI", 12), bd=0, highlightthickness=0, show="•")
        self.pass_entry.pack(side="left", fill="x", expand=True)
        tk.Frame(frame, bg="white", height=1).pack(fill="x", pady=(0,15))

        # Mostrar contraseña
        self.show_password = tk.BooleanVar(value=False)
        tk.Checkbutton(frame, text="Mostrar contraseña", fg="white", bg="#1a1a1a",
                       font=("Segoe UI", 10), selectcolor="#1a1a1a",
                       variable=self.show_password, command=self.toggle_password,
                       bd=0, highlightthickness=0).pack(anchor="w", pady=(0,20))

        # Botones
        login_btn = RoundedButton(frame, text="Login", command=self.login)
        login_btn.pack(pady=10)

        reg_btn = RoundedButton(frame, text="Registrar", command=self.open_register)
        reg_btn.pack(pady=10)

    def toggle_password(self):
        self.pass_entry.config(show="" if self.show_password.get() else "•")

    def login(self):
        user = self.user_entry.get().strip()
        pwd = self.pass_entry.get().strip()
        if not user or not pwd:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos")
            return

        auth = AuthLoginApp()
        user_data, error = auth.login_user(user, pwd)
        if error:
            messagebox.showerror("Error", error)
            return

        # Convertimos tuple a dict para dashboard
        user_dict = {"id": user_data[0], "email": user_data[2]}
        self.destroy()
        dashboard = DashboardApp(user_dict)
        dashboard.mainloop()

    def open_register(self):
        self.destroy()
        reg_window = RegisterApp()
        reg_window.mainloop()


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()


# Aquí puedes definir widgets personalizados para tu app, como barras de progreso, botones, etc.

from tkinter import ttk

class ProgressBar(ttk.Frame):
    def __init__(self, parent, length=300):
        super().__init__(parent)
        self.progress = ttk.Progressbar(self, orient="horizontal", length=length, mode="determinate")
        self.progress.pack()

    def set_value(self, value):
        self.progress['value'] = value


import tkinter as tk
from tkinter import messagebox
class Secundaria(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        tk.Button(
            self, text="Abrir Message bien instanciado",
            command=self.open_good_message).pack(expand=True)
        tk.Button(
            self, text="Abrir Message mal instanciado",
            command=self.open_bad_message).pack(expand=True)
    def open_good_message(self):
        messagebox.showinfo(
            "Test", "Hola aparezco donde debo...", parent=self
            )
    def open_bad_message(self):
        messagebox.showinfo(
            "Test", "Hola aparezco donde no se me espera..."
            )
class Principal(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        tk.Button(
            self, text="Abrir Ventana Secundaria",
            command=self.open_child).pack(fill="both", expand=True)
    def open_child(self):
        sec = tk.Toplevel(self)
        sec.title("Secundaria")
        sec.geometry("650x400+450+350")
        Secundaria(sec).pack(fill="both", expand=True)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Principal")
    root.geometry("650x400+400+300")
    Principal(root).pack(fill="both", expand=True)
    root.mainloop()
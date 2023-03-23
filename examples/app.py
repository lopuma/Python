import tkinter as tk
from showHide import Extracion
from tkinter import ttk
class Aplicacion():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root =  tk.Tk()
        self.root.title("Show and Hide")
        self.root.geometry('1024x768')

        self.cuaderno = ttk.Notebook(self.root)
        self.contenedor = tk.Frame(self.cuaderno, bg='silver')

        self.cuaderno.add(self.contenedor, text="Workspace")
        self.cuaderno.pack(expand=1, fill=tk.BOTH)

        self.btn = tk.Button(self.contenedor, 
            text="ADD EXTRACION", 
            bg='gold',
            command=self.añadir
            )
        self.btn.pack()
    
    def añadir(self):
        extracion = Extracion(self.cuaderno, app)
        self.cuaderno.add(extracion, text='Extracion')
    
    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
        
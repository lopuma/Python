import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import scrolledtext as st
from tkinter.constants import NSEW, NW
from typing import ValuesView
import cambios
from tkinter import *
class FormularioCambios:
    def __init__(self):
        self.articulo1=cambios.Cambios()
        self.ventana1=tk.Tk()
        self.ventana1.title("Registro de cambios")
        self.cuaderno1 = ttk.Notebook(self.ventana1)       
        self.carga_cambios()
        self.consulta_por_cambio()
        self.listado_completo()
        self.cuaderno1.grid(column=0, row=0, padx=10, pady=10)
        self.ventana1.mainloop()
        

    vlist = ["NEW", "SCHED", "IMPL", "IN_PROGRES"]
    clientes = (
            "AFB",
            "ASISA",
            "CESCE",
            "CTTI",
            "ENEL",
            "EUROFRED",
            "FT",
            "GSNI",
            "IGS",
            "IDISO",
            "LBK",
            "PLANETA",
            "SERVIHABITAT",
        )
    def callback(self, event=None):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            self.label.configure(text=data)
        else:
            self.label.configure(text="")
        valorX=data
        print(valorX)
    def carga_cambios(self):
        self.pagina1 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina1, text="Nuevo Registro")
        self.labelframe1=ttk.LabelFrame(self.pagina1, text="Cambios")       
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10, ipadx=100)
        self.lbl1=ttk.Label(self.labelframe1, text="Departamento:")
        self.lbl1.config(foreground='black',background='bisque', font=(15))
        self.lbl1.grid(column=0, row=0, padx=10, pady=20, sticky=NW)
        self.valor1=tk.StringVar()
        self.label = tk.Label(self.labelframe1)
        self.listbox = tk.Listbox(self.labelframe1)
        self.label.grid(column=0, row=0, padx=10)
        self.listbox.grid(column=1, row=0, padx=10)
        self.listbox.insert(0, *self.clientes)
        self.listbox.bind("<<ListboxSelect>>", self.callback)
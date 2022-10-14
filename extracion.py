# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import *
from tkinter import Button, ttk

class Extracion(ttk.Frame):
    def __init__(self, parent, application=None, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args)
        self._application = application
        self.widgets()
    
    def widgets(self):
        self.btn_nav = Button(
            self,
            text="CERRAR PESTAÑA",
            background="#39A2DB",
            border=0,
            borderwidth=0,
            highlightthickness=0,
            relief='flat',
            command=self.cerrar_pestaña
        )
        self.btn_nav.grid(row=0, column=0, sticky="e")

    def cerrar_pestaña(self):
        self._application.cerrar_ventana()

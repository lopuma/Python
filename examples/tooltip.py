import tkinter as tk
from functools import partial
from tkinter import TclError
tool = False
class CustomHovertip(tk.Toplevel):
    def __init__(self, boton, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text
        self.wm_overrideredirect(1)
        self.position_window(boton)

    def showcontents(self):
        label = tk.Label(
            self, text=f' "{self.text}" ', justify=tk.LEFT,
            bg="#151515", fg="#ffffff", relief=tk.SOLID, borderwidth=1,
            font=("Times New Roman", 12)
            )
        label.pack()

    def position_window(self, boton):
        x, y = self.get_position(boton)
        print(x, y)
        root_x = boton.winfo_rootx() + x
        root_y = boton.winfo_rooty() + y
        self.wm_geometry("+%d+%d" % (root_x, root_y))
        self.showcontents()

    def get_position(self, boton):
        return 20, boton.winfo_height() + 1

class Aplicacion():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("450x200")

        self.frame = tk.Frame(self.root, bg="pink")
        self.frame.pack(expand=1, fill=tk.BOTH)
        self.llamar_btn = tk.Button(self.frame, text="Llamar")
        self.llamar_btn.pack(side="top")        
        self.colgar_btn = tk.Button(self.frame, text="Colgar")
        self.colgar_btn.pack(side="left")
        self.llamar_btn.bind("<Motion>", partial(self.openTooltip, self.llamar_btn, "LLAMA SI VAS A LLMAR"))
        self.llamar_btn.bind("<Leave>", self._hide_event)
        self.colgar_btn.bind("<Motion>", partial(self.openTooltip, self.colgar_btn, text="CUELGA SI VAS A COLGAR"))
        self.colgar_btn.bind("<Leave>", self._hide_event)
    
    def _hide_event(self, event=None):
        self.hidetip()
    
    def hidetip(self):
        global tool
        try:
            custom.destroy()
            tool = False
        except TclError:
            pass

    def openTooltip(self, boton, text, *args):
        global custom
        global tool
        if tool == False:
            custom = CustomHovertip(boton, text=text)
            tool = True

    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
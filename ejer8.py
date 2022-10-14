from tkinter import *
from tkinter.messagebox import showinfo
def seleccionar(ev):
    global texto_seleccionado
    texto_seleccionado = ev.widget.get(ANCHOR)
    print(texto_seleccionado)
root = Tk()
listbox = Listbox(root)
listbox.pack(expand=True, fill=BOTH)
listbox.insert(END, 'Primer Elemento de la Lista')
listbox.insert(END, 'Segundo Elemento de la Lista')
texto_seleccionado = 'Ningún elemento Seleccionado'
listbox.bind('<<ListboxSelect>>', seleccionar)
root.bind('<Return>', lambda ev:showinfo(title='Texto Seleccionado', message=texto_seleccionado))
root.mainloop()





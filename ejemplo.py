import tkinter as tk
from tkinter import ttk, messagebox


root = tk.Tk()
root.geometry('335x303')
root.geometry('+560+250')
root.title('Ejemplo quitar selección')
root.maxsize(335, 303)
root.minsize(335, 303)

labelTextInfo = tk.Label(root, text="Ejemplo quitar selección de un item:", font=("Microsoft Sans Serif", 8))
labelTextInfo.place(x=6, y=8)

listboxEjemplo=tk.Listbox(root, font=("Microsoft Sans Serif", 8), borderwidth=2, selectmode='none', activestyle='none', height=13, takefocus=False, highlightthickness=0, exportselection=False)
listboxEjemplo.place(x=9, y=29, width=316)

scrollbarlistboxEjemplo = ttk.Scrollbar(root, orient=tk.VERTICAL)
scrollbarlistboxEjemplo.config(command=listboxEjemplo.yview)
scrollbarlistboxEjemplo.place(x=306, y=31, height=182)

listboxEjemplo.config(yscrollcommand=scrollbarlistboxEjemplo.set) 

for ItemAleatorio in range(15):
    listboxEjemplo.insert(tk.END, ItemAleatorio)

def HabilitarQuitarSeleccion(event=None):
    if len(listboxEjemplo.curselection())!=0:
        btnOkRemoveSelectedItem.config(state='normal', font=("Microsoft Sans Serif", 8))


def QuitarSeleccion(event=None):
    listboxEjemplo.selection_clear(0, tk.END)
    btnOkRemoveSelectedItem.config(state='disabled', font=("MS Sans Serif", 8))

def cerrarVentana(event=None):
    root.destroy()


listboxEjemplo.bind('<Return>', cerrarVentana)
listboxEjemplo.bind('<<ListboxSelect>>', HabilitarQuitarSeleccion)       


btnOkRemoveSelectedItem = tk.Button(root, text='Quitar selección', font=("MS Sans Serif", 8), takefocus=False, width=13, command=QuitarSeleccion, state='disabled')
btnOkRemoveSelectedItem.place(x=158,y=268, height=22)

btnCancelar = tk.Button(root, text='Cancelar', font=("Microsoft Sans Serif", 8), takefocus=False, width=10, command=cerrarVentana)
btnCancelar.place(x=255,y=268, height=22)  

root.mainloop()
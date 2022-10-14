import tkinter as tk

root = tk.Tk()
root.minsize(height = 400, width = 200)
def funcion(event):
    def liberar_entry(event):
        widget.fijar_posicion = False
        widget.config(state="normal") # Habilitar listbox
        event.widget.place_forget()   # Eliminar Entry
    widget = event.widget
    print(widget)
    widget.fijar_posicion = True
    print(widget.fijar_posicion )
    widget.config(state="disabled")
    # Genera las coordenadas para la entrada
    item = widget.curselection()[0]
    alto_celda = 16
    cantidad_items = len(widget.get(0, tk.END))
    fraccion_item = 1/cantidad_items
    fracciones = widget.yview()
    item_inicial = fracciones[0]/fraccion_item
    diferencia_hasta_item = item - item_inicial
    coor_listbox_x = widget.winfo_x()
    coor_listbox_y = widget.winfo_y()
    # Crea la entrada
    entrada = tk.Entry(root)
    entrada.place(x = coor_listbox_x + 2,
                  y = coor_listbox_y + alto_celda * diferencia_hasta_item + 2,
                  width = 100 - 4,
                  height = alto_celda
                  )
    entrada.focus_set()
    entrada.bind("<Return>", liberar_entry)
def _on_scroll(event):
    if listbox.fijar_posicion:
        return "break"
def _listbox_yview(*args, **kwargs):
    if not listbox.fijar_posicion:
        listbox.yview(*args, **kwargs)
listbox = tk.Listbox(root)
listbox.fijar_posicion = False
listbox.place(x = 10, y = 10, width = 100, height = 300)
listbox.bind("<MouseWheel>", _on_scroll) # rueda ratón
listbox.bind("<Button-4>", _on_scroll)   # rueda ratón en sistemas x11
listbox.bind("<Button-5>", _on_scroll)   # rueda ratón en sistemas x11
listbox.bind("<B1-Leave>", _on_scroll)   # desplazamiento automático
scroll_y = tk.Scrollbar(root)
scroll_y.place(x = 10 + 100, y = 10, height = 300)
listbox.configure(yscrollcommand = scroll_y.set)
scroll_y.config(command = _listbox_yview)
print(listbox.fijar_posicion)
for i in range(0, 30):
    listbox.insert(tk.END, i)
listbox.bind('<Double-Button-1>', funcion)
root.mainloop()



import tkinter as tk

# esta función da el resultado redondeado hacia arriba de una división
def ceildiv(dividendo, divisor):
    # divmod nos devuelve una tupla con el cociente y el resto, desempaquetamos eso.
    cociente, resto = divmod(dividendo, divisor)

    # sumamos al cociente el resto convertido en booleano. Recuerda que True vale 1 y False 0.
    # Por lo que si hay resto se sumará 1.
    return cociente + bool(resto)

def grid_by_column(frame, columns, spacex=10, spacey=10):
    # obtenemos todos los widgets del frame
    widgets = frame.winfo_children()
    print(widgets)
    rows = ceildiv(len(widgets), columns)

    row = 0
    column = 0

    for widget in widgets:
        # ubicamos el widget en la esquina noroeste de la celda.
        widget.grid(row=row, column=column, sticky="nw")

        # el siguiente widget será ubicado en la siguiente columna.
        column += 1

        # si alcanzamos la cantidad maxima de columnas...
        if(column >= columns):
            column = 0
        
            row += 1

    # le agregamos un espacio (en este caso a la derecha) a cada fila menos la ultima.
    # La ultima se omite para evitar que el frame tenga espacio vacío en el borde derecho.
    for row in range(rows-1):
        frame.rowconfigure(row, pad=spacex)

    # se hace lo mismo con las columnas. Se omite la ultima para evitar que haya espacio vacío en el borde inferior.
    for column in range(columns-1):
        frame.columnconfigure(column, pad=spacey)

root = tk.Tk()
frame = tk.Frame()
list = []
list.append("hola")
list.append("chao")
list.append("rtr")
list.append("chao")
list.append("dfd")

print(list)
for i in list:
    tk.Button(frame, text=i, width=2)

grid_by_column(frame, 3)
frame.pack()

root.mainloop()
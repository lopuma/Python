import sqlite3
import tkinter as tk


def compras():
    def yscroll_hora_entrada(*args):
        wyview = listbox_hora_entrada.yview()
        if  listbox_indice.yview() != wyview:
            listbox_indice.yview_moveto(args[0])
        if listbox_hora_salida.yview() != wyview:
            listbox_hora_salida.yview_moveto(args[0])
        scroll.set(*args)

    def yscroll_hora_salida(*args):
        wyview = listbox_hora_salida.yview()
        if  listbox_indice.yview() != wyview:
            listbox_indice.yview_moveto(args[0])
        if listbox_hora_entrada.yview() != wyview:
            listbox_hora_entrada.yview_moveto(args[0])
        scroll.set(*args)

    def yscroll_indice(*args):
        wyview = listbox_indice.yview()
        if listbox_hora_salida.yview() != wyview:
            listbox_hora_salida.yview_moveto(args[0])
        if listbox_hora_entrada.yview() != wyview:
            listbox_hora_entrada.yview_moveto(args[0])
        scroll.set(*args)

    def yview(*args):
        listbox_indice.yview(*args)
        listbox_hora_entrada.yview(*args)
        listbox_hora_salida.yview(*args)

    # Se borran los elementos de la ventana anterior
    #BotonCompras.place_forget()
    #BotonVentas.place_forget()

    #Selecciono la información de la base de datos
    cursor = conn.execute("select * from Compras")

    # Defino listas y scrollbar
    listbox_indice = tk.Listbox(root, bg='beige', yscrollcommand=yscroll_indice)
    listbox_hora_entrada = tk.Listbox(root, bg='beige', yscrollcommand=yscroll_hora_entrada)
    listbox_hora_salida = tk.Listbox(root, bg='beige', yscrollcommand=yscroll_hora_salida)
    scroll = tk.Scrollbar(root, command=yview)

    # Ingreso datos en las listas   
    i = 1
    for i, (ind, hent, hsal) in enumerate(cursor):
        listbox_indice.insert(i, ind)
        listbox_hora_entrada.insert(i, hent)
        listbox_hora_salida.insert(i, hsal)

    # Tamaño y ubicación de los elementos
    listbox_indice.place(x=10, y=5, width=30, height=300)
    listbox_hora_entrada.place(x=40, y=5, width=100, height=300)
    listbox_hora_salida.place(x=140, y=5, width=100, height=300)
    scroll.place(x=230, y=5, height=300)


if __name__ == "__main__":
    from random import randrange
    import datetime 

    root = tk.Tk()
    root.geometry("255x310")
    conn = sqlite3.connect(':memory:')

    sql = """
    CREATE TABLE Compras (
    id integer PRIMARY KEY,
    hora_entrada text,
    hora_salida text
    );
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    sql = ''' INSERT INTO Compras(id, hora_entrada, hora_salida)
                VALUES(?,?,?) '''

    def random_time():
        s = datetime.datetime(2019, 1, 1, 0, 0, 0)
        return (s + datetime.timedelta(seconds=randrange(86400))).strftime("%H:%M:%S")

    l = [(n, random_time(), random_time()) for n in range(1, 50)]
    cursor.executemany(sql, l)
    conn.commit()
    cursor.close()

    compras()
    root.mainloop()
    conn.close()
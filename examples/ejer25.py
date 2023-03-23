import tkinter as tk
import json
from tkinter import ttk
from tkinter import *

class Ventana():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CONTINOUS COMPLIANCE")
        self.root.geometry("870x300")
        self.widgets_ventanas()
    
    def widgets_ventanas(self):

        # creamos boton mostrar listas
        self.btnBuscar = ttk.Button(
            self.root,
            text='Mostrar',
            command=self.cargar_ventanas
        )
        self.btnBuscar.grid(row=0, column=0, sticky=W)

        ## --- creamos el scrollbar
        self.tree_scrollbar=tk.Scrollbar(self.root, orient=tk.VERTICAL)
        self.tree_scrollbar.grid(column=0, row=1, sticky=N+S,padx=(0,5), pady=10)
        
        ## ---creamos el treeview
        self.tree = ttk.Treeview(
            self.root, 
            yscrollcommand=self.tree_scrollbar.set,
            height=10,
        )
        ## ---configuramos el scroll al trieview
        self.tree_scrollbar.config(command=self.tree.yview)
        ## ---creamos las columnas
        self.tree['columns'] = ("NAME","OWNER","TIPO","OWNERGROUP","CODE")
        ## --- formato a las columnas
        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column("NAME", anchor=W, width=350)
        self.tree.column("OWNER", anchor=CENTER, width=150)
        self.tree.column("TIPO", anchor=CENTER, width=100)
        self.tree.column("OWNERGROUP", anchor=CENTER, width=150)
        self.tree.column("CODE", anchor=CENTER, width=100)
        ## --- indicar cabecera
        self.tree.heading("#0", text="", anchor=W)
        self.tree.heading("#1", text="NAME", anchor=W)
        self.tree.heading("#2", text="OWNER", anchor=CENTER)
        self.tree.heading("#3", text="TIPO", anchor=CENTER)
        self.tree.heading("#4", text="OWNER GROUP", anchor=CENTER)
        self.tree.heading("#5", text="CODE", anchor=CENTER)
        self.tree.tag_configure('oddrow', background="#CEE5D0", font=('Verdana', 14))
        self.tree.tag_configure('evenrow', background="#F3F0D7", font=('Verdana', 14))
        
        self.tree.grid(column=0, row=1, pady=10, padx=(5,0), sticky=E+W)

    def limpiar_tree(self):
        records = self.tree.get_children()
        for elemnt in records:
            self.tree.delete(elemnt)
    
    def cargar_ventanas(self):

        #limpiando el arbol de vistas
        self.limpiar_tree()

        #Cargar datos desde el archivo JSON
        with open('directory.json') as g:
                data = json.load(g)
                count = 0
                #aqui eleginos el cliente que queremos
                for md in data['INFRA']:
                    
                    #guardar solo el valor de 'object a una lista'
                    if count % 2 == 0:
                        self.tree.insert(parent='', index='end', iid=count, text='', value=(md['object'],md['owner'],md['tipo'],md['ownerGroup'],md['code']), tags=('evenrow'))
                    else:
                        self.tree.insert(parent='', index='end', iid=count, text='', value=(md['object'],md['owner'],md['tipo'],md['ownerGroup'],md['code']), tags=('oddrow'))
                    count += 1

    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Ventana()
    app.mainloop()
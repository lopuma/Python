import tkinter
from tkinter import ttk
import os
class visual(object):
    def __init__(self,path):
        #Crear ventana
        self.win=tkinter.Tk()
        self.win.geometry('400x400')
        self.win.title ('Interfaz visual')
                 # Crea un diagrama de árbol
        self.tree=tkinter.ttk.Treeview()
        self.tree.pack()
                 #Extraiga el último nombre de archivo en la ruta
        temppath=os.path.basename(path)
                 # Nombre de archivo a atravesar rama de primer nivel
        treeF = self.tree.insert('', 0, text=temppath)
                 # Llamar a la función ergódica, pasar el nombre de la rama
        self.ergodic(path,treeF)
        self.win.mainloop()
    def ergodic(self,path,root):
        # Ponga los archivos de la carpeta en la lista
        filelist=os.listdir(path)
        for filename in filelist:
            #Espere hasta la ruta absoluta del archivo
            abspath=os.path.join(path,filename)
            #Está dentro de la rama raíz
            treeFinside = self.tree.insert(root, 0, text=filename,values=(abspath))
            print(os.path.isdir(abspath))
            if os.path.isdir(abspath):
                # Devuelve la ruta y el árbol dentro del nombre de la rama del nivel superior
                self.ergodic(abspath,treeFinside)

a=visual('/home/esy9d7l1/compliance/extracion')
import tkinter as tk
from tkinter import messagebox
from tabview import tabview
# Genere una función de widget en el cuerpo, el widget devuelto se agregará al cuerpo de la vista de pestaña
def create_body():
    global body
    return tk.Label(body, text="this is body")
# Devolución de llamada cuando se hace clic en la pestaña
def select(index):
    print("current selected -->", index)
# La devolución de llamada cuando se elimina la pestaña, no se eliminará si devuelve False
def remove(index):
    print("remove tab -->", index)
    if messagebox.askokcancel("título", "¿Estás seguro de que deseas cerrar esta pestaña?"):
        return True
    else:
        return False
# ----------------------- Ejemplo de uso ------------------------ ----
root = tk.Tk()
root.geometry("640x300")
tab_view = tabview(root, generate_body=create_body,
                   select_listen=select, remove_listen=remove)
body = tab_view.body
label_1 = tk.Label(tab_view.body, text="this is tab1")
label_2 = tk.Label(tab_view.body, text="this is tab2")
# El primer parámetro es el widget agregado al cuerpo, y el segundo parámetro es el título de la pestaña
tab_view.add_tab(label_1, "tabs1")
tab_view.add_tab(label_2, "tabs2")
# TabView debe completarse en las direcciones x e y, y expandir debe establecerse en yes
tab_view.pack(fill="both", expand='yes', pady=2)
root.mainloop()
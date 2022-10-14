from cgitb import text
import functools
import tkinter as tk
from tkinter import ttk
root= tk.Tk()

limit_before_list = [0]
max_posts_list = [0]
max_comments_list = [0]
limit_before = 'limit_before'
max_posts = 'max_posts'
max_comments = 'max_comments'
def mostrar_nombre(pestaña, event):
    listbox = event.widget
    index = listbox.curselection()
    value = listbox.get(index[0])
    print(pestaña)  # Aca esta mi problema, me devuelve la ultima ingresada
    print(value)
pestañas = {
    limit_before: range(0, 160, 10),
    max_posts: range(0, 410, 10),
    max_comments: range(0, 4100, 100),
}
note = ttk.Notebook()
for pestaña, items in pestañas.items():
    frame = ttk.Frame(note)
    note.add(frame, text=pestaña)
    listbox = tk.Listbox(frame, exportselection=False)
    listbox.grid(row=0, column=0)
    listbox.bind("<<ListboxSelect>>", functools.partial(mostrar_nombre, pestaña))
    for item in items:
        listbox.insert(tk.END, item)
def añadir():
    contenedor= ttk.Frame(note)
    note.add(contenedor, text='nueva pestaña')
    listbox = tk.Listbox(contenedor, exportselection=False)
    listbox.grid(row=0, column=0)
    print(listbox)
    listbox.bind("<<ListboxSelect>>", functools.partial(mostrar_nombre, pestaña))
    anadir1(listbox)

def anadir1(listbox):
    val = listbox
    listbox.insert(tk.END, val)

def anadir2():
    listbox.insert(tk.END, "item5")
    listbox.insert(tk.END, "item6")
    listbox.insert(tk.END, "item7")
    listbox.insert(tk.END, "item8")

bt = tk.Button(
    root,
    text='add',
    command=añadir
)
bt.pack(fill='both', side='left')
bt1 = tk.Button(
    root,
    text='add1',
    command=anadir1
)
bt1.pack(fill='both', side='left')
bt2 = tk.Button(
    root,
    text='add2',
    command=anadir2
)
bt2.pack(fill='both', side='left')
note.pack()
note.mainloop()










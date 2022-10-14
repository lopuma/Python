import functools
import tkinter as tk
from tkinter import ttk
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
note.pack()
note.mainloop()
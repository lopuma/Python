from tkinter import *
# Importar ttk
from tkinter import ttk
# Importar cuadro de mensaje de importación
from tkinter import messagebox
# Importar ImageTk, Imagen
from PIL import Image, ImageTk
# Importar archivo de diálogo
from tkinter import filedialog
import os

path = os.path.expanduser("~/")
path_icon = path+"compliance/image/"

class App:
    def __init__(self, master):
        self.master = master
        self.init_menu()

    # Crear menú
    def init_menu(self):
        # Crear barra de menú, se coloca en self.master
        menubar = Menu(self.master)
        # Importar icono de elemento de menú
        self.master.filenew_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"OpenDesviaciones.png").resize((20, 20)))
        self.master.fileopen_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"OpenDesviaciones.png").resize((20, 20)))
        # Agregar barra de menú
        self.master['menu'] = menubar
        # Crear menú file_menu, se coloca en la barra de menú
        file_menu = Menu(menubar, tearoff=0)
        # Use el método add_cascade para agregar el menú file_menu
        menubar.add_cascade(label='archivo', menu=file_menu)
        # Crea el menú lang_menu, se coloca en la barra de menú
        lang_menu = Menu(menubar, tearoff=0)
        # Use el método add_cascade para agregar el menú lang_menu
        menubar.add_cascade(label='Elija un idioma', menu=lang_menu)
        # Use el método add_command para agregar elementos de menú a file_menu
        file_menu.add_command(label='Nuevo', command=self.create_newfile,  # Vincular métodos de manejo de eventos para elementos de menú
                              image=self.master.filenew_icon,  # Insertar icono para elemento de menú
                              compound=LEFT)  # Coloque el icono en el lado izquierdo del texto
        file_menu.add_command(label='encender', command=self.open_file,  # Vincular métodos de manejo de eventos para elementos de menú
                              image=self.master.fileopen_icon,  # Insertar icono para elemento de menú
                              compound=LEFT)  # Coloque el icono en el lado izquierdo del texto
        # Use el método add_separator para agregar divisor a file_menu
        file_menu.add_separator()
        # Crea un menú de palabras para file_menu
        sub_menu = Menu(file_menu, tearoff=0)
        # Use el método add_cascade para agregar submenús a file_menu
        file_menu.add_cascade(label='Elige un juego', menu=sub_menu)
        self.gameVar = IntVar()
        self.games = ['LOL', 'DNF', 'PUBG']
        # Use el bucle para agregar elementos de menú al submenú sub_menu
        for i, m in enumerate(self.games):
            # Use el método add_radiobutton para agregar elementos de menú al submenú sub_menu
            # Vincular la misma variable, indicando que son un grupo
            sub_menu.add_radiobutton(label=m, command=self.choose_game,  # Vincular métodos de manejo de eventos para elementos de menú
                                     variable=self.gameVar, value=i)
        self.langVars = [StringVar(), StringVar(), StringVar(), StringVar()]
        # Use un bucle para agregar elementos de menú al menú lang_menu
        for i, m in enumerate(['English','Chinese']):
            # Use el método add_checkbutton para agregar varios elementos del menú de selección al menú lang_menu
            lang_menu.add_checkbutton(label=m, command=self.choose_lang,  # Métodos de manejo de eventos vinculantes para elementos de menú de lang_menu
                                      onvalue=m, variable=self.langVars[i])

    def choose_game(self):
        messagebox.showinfo(message='El juego seleccionado es:% s' % self.games[self.gameVar.get()])

    def choose_lang(self):
        rt_list = [e.get() for e in self.langVars]
        messagebox.showinfo(message='El idioma seleccionado es:% s' % ','.join(rt_list))

    def create_newfile(self):
        filedialog.asksaveasfile(title='Nuevo', filetypes=[('Archivo de texto', '*.txt'), ('Archivo fuente de Python', '*.py')], initialdir='d:/')

    def open_file(self):
        filedialog.askopenfile(title='encender', filetypes=[('Archivo de texto', '*.txt'), ('Archivo fuente de Python', '*.py')], initialdir='d:/')


root = Tk()
root.title('Prueba de menú')
root.geometry('400x200')
# Prohibir cambiar el tamaño de la ventana
root.resizable(width=False, height=False)
App(root)
root.mainloop()
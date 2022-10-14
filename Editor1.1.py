import tkinter as tk
import tkinter.font as tkFont

####### Python 2 #######
#import Tkinter as tk
#import tkFont  



def beep_error(f):
    '''
    Decorador que permite emitir un beep cuando un método de instancia
    decorado de un widget produce una excepción
    '''
    def applicator(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except:
            if args and isinstance(args[0], tk.Widget):
                args[0].bell()
    return applicator

class MyText(tk.Text):
    def __init__(self, parent=None, *args, **kwargs):
        tk.Text.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.bind('<Control-a>', self.seleccionar_todo)
        self.bind('<Control-x>', self.cortar)
        self.bind('<Control-c>', self.copiar)
        self.bind('<Control-v>', self.pegar)
        self.bind('<Control-z>', self.deshacer)
        self.bind('<Control-Shift-z>', self.rehacer)
        self.bind("<Button-3><ButtonRelease-3>", self.mostrar_menu)

    def mostrar_menu(self, event):
        '''
        Muestra un menú popup con las opciones copiar, pegar y cortar
        al hacer click derecho en el Text
        '''
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Cortar", command=self.cortar)
        menu.add_command(label="Copiar", command=self.copiar)
        menu.add_command(label="Pegar", command=self.pegar)
        menu.tk.call("tk_popup", menu, event.x_root, event.y_root)

    def copiar(self, event=None):
        self.event_generate("<<Copy>>")
        self.see("insert")
        return 'break'

    def cortar(self, event=None):
        self.event_generate("<<Cut>>")
        return 'break'

    def pegar(self, event=None):
        self.event_generate("<<Paste>>")
        self.see("insert")
        return 'break'

    def seleccionar_todo(self, event=None):
        self.event_generate("<<SelectAll>>")
        #self.tag_add('sel', '1.0', 'end')   # < Otra alternativa
        return 'break'

    @beep_error
    def deshacer(self, event=None):
        self.tk.call(self, 'edit', 'undo')
        return 'break'

    @beep_error
    def rehacer(self, event=None):
        self.tk.call(self, 'edit', 'redo')
        return 'break'

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        menubar = tk.Menu(self, bg='black', fg='white')
        self.config(menu=menubar)

        editmenu = tk.Menu(menubar, tearoff=0, bg='black', fg='white')
        menubar.add_cascade(label='Editar', menu=editmenu, underline=0)


        frame = tk.Frame(self, bg='black')
        frame.pack(fill='both', expand=1)
        frame.config(padx=10, pady=10)

        frame_txt = tk.Frame(frame, background='black')
        frame_txt.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W+tk.E)

        self.text_font = tkFont.Font(family='Consolas', size=12)
        self.text_01 = MyText(frame_txt, wrap=tk.WORD, bd=0, undo=True)
        self.text_01.pack(fill='both', expand=1)
        self.text_01.config(bd=0, padx=6, pady=4, font=self.text_font,
                            selectbackground='lightblue',
                            width=44, height=16,
                            bg='#242424', fg='white',
                            insertbackground='white',
                            highlightbackground='black',
                            highlightcolor='white'
                            )

        editmenu.add_command(label='Deshacer',
                            command=self.text_01.deshacer,
                            accelerator='Ctrl+Z'
                            )
        editmenu.add_command(label='Rehacer',
                            command=self.text_01.rehacer,
                            accelerator='Ctrl+Shift+Z'
                            )
        editmenu.add_separator()
        editmenu.add_command(label='Cortar',
                            command=self.text_01.cortar,
                            accelerator='Ctrl+X'
                            )
        editmenu.add_command(label='Copiar',
                            command=self.text_01.copiar,
                            accelerator='Ctrl+C'
                            )
        editmenu.add_command(label='Pegar',
                            command=self.text_01.pegar,
                            accelerator='Ctrl+V'
                            )
        editmenu.add_command(label='Seleccionar todo',
                            command=self.text_01.seleccionar_todo,
                            accelerator='Ctrl+A'
                            )



if __name__ == "__main__":
    MainApp().mainloop()
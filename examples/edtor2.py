# -*- coding: utf-8 -*-
'''
####### Python 3 #######
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox as MessageBox

'''
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox as MessageBox
####### Python 2 #######
# import Tkinter as tk
# import tkFont
# import tkMessageBox as MessageBox



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
    def __init__(self, parent=None, app=None, *args, **kwargs):
        tk.Text.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.app = app

        self.bind('<Control-a>', self.seleccionar_todo)
        self.bind('<Control-x>', self.cortar)
        self.bind('<Control-c>', self.copiar)
        self.bind('<Control-v>', self.pegar)
        self.bind('<Control-z>', self.deshacer)
        self.bind('<Control-Shift-z>', self.rehacer)
        self.bind("<Button-3><ButtonRelease-3>", self.mostrar_menu)


        self._ocurrencias_encontradas = []
        self._numero_ocurrencia_actual = None


    @property
    def numero_ocurrencias(self):
        return len(self._ocurrencias_encontradas)

    @property
    def numero_ocurrencia_actual(self):
        return self._numero_ocurrencia_actual

    @property
    def indice_ocurrencia_actual(self):
        tags = self.tag_ranges('found_prev_next')
        return tags[:2] if tags else None

    @indice_ocurrencia_actual.setter
    def indice_ocurrencia_actual(self, idx):
        # establecer la marca distintiva para la ocurrencia a etiquetar
        self.elim_tags(['found_prev_next'])
        self.tag_config('found_prev_next', background='orangered')

        if idx is not None:
            self.tag_add('found_prev_next', *idx)
            self.see(idx[0])
            self._numero_ocurrencia_actual = self._ocurrencias_encontradas.index(self.indice_ocurrencia_actual) + 1
        else:
            self._numero_ocurrencia_actual = None

    @property
    def ocurrencias_encontradas(self):
        return self._ocurrencias_encontradas


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
        self.tag_add('sel', '1.0', 'end')
        return 'break'

    @beep_error
    def deshacer(self, event=None):
        self.tk.call(self, 'edit', 'undo')
        return 'break'

    @beep_error
    def rehacer(self, event=None):
        self.tk.call(self, 'edit', 'redo')
        return 'break'

    def get_index(self, index):
        '''Dado un índice en cualquier formato retorna una tupla (fila -> int, columna -> int)'''
        return tuple(int(idx) for idx in self.index(index).split("."))


    def buscar_todo(self, txt_buscar=None):
        '''Buscar todas las ocurrencias en el Entry de MainApp'''

        # eliminar toda marca establecida, si existiera, antes de plasmar nuevos resultados
        self.elim_tags(['found', 'found_prev_next'])

        if txt_buscar:
            # Contador total de resultados
            # empezar desde el principio (y parar al llegar al final [stopindex >> END])
            idx = '1.0'
            len_ocurr = tk.IntVar()
            while True:
                # encontrar siguiente ocurrencia, salir del loop si no hay más
                idx = self.search(txt_buscar, idx, count=len_ocurr, nocase=1, stopindex=tk.END)
                if not idx: break
                # index justo después del final de la ocurrencia
                lastidx = '%s+%dc' % (idx, len_ocurr.get())
                # etiquetando toda la ocurrencia (incluyendo el start, excluyendo el stop)
                self.tag_add('found', idx, lastidx)
                # preparar para buscar la siguiente ocurrencia
                idx = lastidx

            # configurando la forma de etiquetar las ocurrencias encontradas
            self.tag_config('found', background='dodgerblue')

        tags = self.tag_ranges('found')
        self._ocurrencias_encontradas = list(zip(*[iter(tags)] * 2))

        self.buscar_next()


    def buscar_prev(self):
        '''Buscar previa ocurrencia en el Entry de MainApp'''
        idx = self.indice_ocurrencia_actual[0] if self.indice_ocurrencia_actual else self.index(tk.INSERT)    
        self.indice_ocurrencia_actual = self.tag_prevrange('found', idx) or self.tag_prevrange('found', self.index(tk.END)) or None


    def buscar_next(self):
        '''Buscar siguiente ocurrencia en el Entry de MainApp'''
        idx = self.indice_ocurrencia_actual[1] if self.indice_ocurrencia_actual else self.index(tk.INSERT)    
        self.indice_ocurrencia_actual = self.tag_nextrange('found', idx) or self.tag_nextrange('found', "0.0") or None


    def reemplazar(self, txt_reemplazar=None, all=False):
        '''Reemplazo de ocurrencia(s) por otro término'''
        if not all and self.indice_ocurrencia_actual is not None:
            start, end = self.indice_ocurrencia_actual
            self._ocurrencias_encontradas.remove(self.indice_ocurrencia_actual)
            self.delete(start, end)
            self.insert(start, txt_reemplazar)
            tags = self.tag_ranges('found')
            self.buscar_next()


        elif all:
            for start, end in reversed(self.ocurrencias_encontradas):
                self.delete(start, end)
                self.insert(start, txt_reemplazar)
                self._ocurrencias_encontradas  = []
                self.indice_ocurrencia_actual = None


    def elim_tags(self, l_tags):
        '''Eliminar etiqueta(s) pasada(s)'''
        for l_tag in l_tags:
            self.tag_delete(l_tag)



class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        menubar = tk.Menu(self, bg='black', fg='white')
        self.config(menu=menubar)

        editmenu = tk.Menu(menubar, tearoff=0, bg='black', fg='white')
        menubar.add_cascade(label='Editar', menu=editmenu, underline=0)

        findmenu = tk.Menu(menubar, tearoff=0, bg='black', fg='white')
        menubar.add_cascade(label='Buscar', menu=findmenu, underline=0)


        frame = tk.Frame(self, bg='black')
        frame.pack(fill='both', expand=1)
        frame.config(padx=10, pady=10)

        frame_txt = tk.Frame(frame, background='black')
        frame_txt.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W+tk.E)

        self.text_font = tkFont.Font(family='Consolas', size=12)
        self.text_01 = MyText(frame_txt, app=self, wrap=tk.WORD, bd=0, undo=True)
        self.text_01.pack(fill='both', expand=1)
        self.text_01.config(bd=0, padx=6, pady=4, font=self.text_font,
                            selectbackground='lightblue',
                            width=44, height=16,
                            bg='#242424', fg='white',
                            insertbackground='white',
                            highlightbackground='black',
                            highlightcolor='white'
                            )

        self.text_01.bind('<Control-f>', lambda x: self.buscar_reemplazar(False))
        self.text_01.bind('<Control-h>', lambda x: self.buscar_reemplazar(True))

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

        findmenu.add_command(label='Buscar',
                            command=self.buscar_reemplazar,
                            accelerator='Ctrl+F'
                            )
        findmenu.add_command(label='Buscar y Reemplazar',
                            command=lambda: self.buscar_reemplazar(True),
                            accelerator='Ctrl+H'
                            )

        # Cargando un texto de prueba
        text_01_contenido = '''[INICIO]
        01- Esto es un contenido de prueba para buscar cualquier texto.

        02- Unas cuántas palabras que forman frases y párrafos en los que buscar concurrencias referidas a los términos buscados.


        03- Esto es un contenido de prueba para buscar cualquier texto.

        04- Unas cuántas palabras que forman frases y párrafos en los que buscar concurrencias referidas a los términos buscados.


        05- Esto es un contenido de prueba para buscar cualquier texto.

        06- Unas cuántas palabras que forman frases y párrafos en los que buscar concurrencias referidas a los términos buscados.

        [ES el FIN]'''
        self.text_01.insert(1.0, text_01_contenido)

        # Para evitar que se abran más de un panel de bus_reem_top
        self.bus_reem_top_on = False

    #ventana BUSCAR
    def buscar_reemplazar(self, con_reemplazo=None, event=None):
        '''Panel de búsqueda/reemplazo de términos en el Text'''
        print(con_reemplazo)
        if not self.bus_reem_top_on:

            bus_reem_top_w = 360
            bus_reem_top_h = 80
            bus_reem_top_tit = 'Buscar'
            bus_reem_top_msg_w = 240

            if con_reemplazo:
                bus_reem_top_h = 120
                bus_reem_top_tit = 'Buscar y Reemplazar'
                bus_reem_top_msg_w = 280

            bus_reem_top_x = (self.winfo_screenwidth() // 2) - (bus_reem_top_w // 2)
            bus_reem_top_y = (self.winfo_screenheight() // 2) - (bus_reem_top_h // 2)

            self.bus_reem_top = tk.Toplevel(self)
            # Considerando evento de cierre de la ventana
            self.bus_reem_top.protocol('WM_DELETE_WINDOW', self.on_closing_bus_reem_top)
            self.bus_reem_top.geometry('{}x{}+{}+{}'.format(bus_reem_top_w, bus_reem_top_h, bus_reem_top_x, bus_reem_top_y))
            self.bus_reem_top.config(bg='white', padx=5, pady=5)
            self.bus_reem_top.resizable(1,1)

            self.bus_reem_frm_tit = tk.Frame(self.bus_reem_top, bg='grey', pady=5)
            self.bus_reem_frm_tit.pack(fill='x', expand=1)

            # ¿¿Cómo centrar este Frame o su contenido??
            self.bus_reem_frm_busca = tk.Frame(self.bus_reem_top, bg='grey', padx=5, pady=5)
            self.bus_reem_frm_busca.pack(fill='x', expand=1)

            self.bus_reem_top.title('{}...'.format(bus_reem_top_tit))
            self.bus_reem_num_results = tk.StringVar()
            self.bus_reem_num_results.set('~ {} ~'.format('Sin resultados'))

            #bus_reem_top_msg = tk.Message(self.bus_reem_frm_tit, textvariable=self.bus_reem_num_results, bg=_cfg__._root_color_quater, padx=10, pady=0)  # <<<<<<<<<<<<<< comentado para no depender de _cgfg__
            bus_reem_top_msg = tk.Message(self.bus_reem_frm_tit, textvariable=self.bus_reem_num_results, padx=10, pady=0)                                 # <<<<<<<<<<<<<<
            bus_reem_top_msg.pack(fill='both', expand=1)
            bus_reem_top_msg.config(width=bus_reem_top_msg_w, justify='center', font=('Consolas', 14, 'bold'))

            self.entr_str_busca = tk.Entry(self.bus_reem_frm_busca)
            self.entr_str_busca.grid(row=0, column=0, padx=3)

            # Si hay un texto seleccionado...
            if self.text_01.tag_ranges('sel'):
                TXT_seleccionado = self.text_01.get(tk.SEL_FIRST, tk.SEL_LAST)
                # Rellenando la caja si hay algo seleccionado en el Text
                self.entr_str_busca.insert(0, TXT_seleccionado)
                self._buscar()
                self._buscar_anterior()

            self.btn_buscar_todo = tk.Button(self.bus_reem_frm_busca, text='Buscar', command=self._buscar)
            self.btn_buscar_todo.grid(row=0, column=1, padx=3)
            self.btn_buscar_prev = tk.Button(self.bus_reem_frm_busca, text='<|', command=self._buscar_anterior)
            self.btn_buscar_prev.grid(row=0, column=2, padx=3)
            self.btn_buscar_next = tk.Button(self.bus_reem_frm_busca, text='|>', command=self._buscar_siguiente)
            self.btn_buscar_next.grid(row=0, column=3, padx=3)

            self.entr_str_busca.focus_set()

            # Bindings
            # Considerando evento tras soltar cualquier tecla pulsada
            # dentro del entr_str_busca
            self.entr_str_busca.bind('<Any-KeyRelease>', self.on_entr_str_busca_key_release)
            self.bus_reem_top.bind('<KeyRelease-F2>', self._buscar_anterior)
            self.bus_reem_top.bind('<KeyRelease-F3>', self._buscar_siguiente)

            if con_reemplazo:
                self.bus_reem_frm_reempl = tk.Frame(self.bus_reem_top, bg='grey', padx=5, pady=5)
                self.bus_reem_frm_reempl.pack(fill='x', expand=1)

                self.entr_str_reempl = tk.Entry(self.bus_reem_frm_reempl)
                self.entr_str_reempl.grid(row=1, column=0, padx=3)
                self.btn_reemplazar_next = tk.Button(self.bus_reem_frm_reempl, text='Reemplazar', command=self._reemplazar)
                self.btn_reemplazar_next.grid(row=1, column=1, padx=2)
                self.btn_reemplazar_todo = tk.Button(self.bus_reem_frm_reempl, text='Reemplazar todo', command=self._reemplazar_todo)
                self.btn_reemplazar_todo.grid(row=1, column=2, padx=2)

            # Para evitar que se abran más de un panel de bus_reem_top
            self.bus_reem_top_on = True

        # Para que el evento no se propague
        return 'break'

    def on_closing_bus_reem_top(self):
        '''En el momento de cerrar el cuadro de búsqueda'''
        if MessageBox.askokcancel('Quit', '¿Cerrar el panel de búsqueda?'):
            # borrando toda etiqueta establecida en los resultados de búsqueda
            self.text_01.elim_tags(['found', 'found_prev_next'])
            # cerrando búsqueda
            self.bus_reem_top.destroy()

            # Para evitar que se abran más de un panel de bus_reem_top
            self.bus_reem_top_on = False

    def on_entr_str_busca_key_release(self, event):
        if event.keysym != "F2" and event.keysym != "F3":  # F2 y F3
            self._buscar()
            return "break"

    def _buscar(self, event=None):
        self.text_01.buscar_todo(self.entr_str_busca.get())
        if self.text_01.ocurrencias_encontradas:
            self.bus_reem_num_results.set('~ {} de {} ~'.format(self.text_01.numero_ocurrencia_actual, self.text_01.numero_ocurrencias))
        else:
            self.bus_reem_num_results.set('~ {} ~'.format('Sin resultados'))

    def _buscar_siguiente(self, event=None):
        self.text_01.buscar_next()
        if self.text_01.ocurrencias_encontradas:
            self.bus_reem_num_results.set('~ {} de {} ~'.format(self.text_01.numero_ocurrencia_actual, self.text_01.numero_ocurrencias))
        else:
            self.bus_reem_num_results.set('~ {} ~'.format('Sin resultados'))

    def _buscar_anterior(self, event=None):
        self.text_01.buscar_prev()
        if self.text_01.ocurrencias_encontradas:
            self.bus_reem_num_results.set('~ {} de {} ~'.format(self.text_01.numero_ocurrencia_actual, self.text_01.numero_ocurrencias))
        else:
            self.bus_reem_num_results.set('~ {} ~'.format('Sin resultados'))

    def _reemplazar(self, event=None):
        self.text_01.reemplazar(self.entr_str_reempl.get())
        if self.text_01.ocurrencias_encontradas:
            self.bus_reem_num_results.set('~ {} de {} ~'.format(self.text_01.numero_ocurrencia_actual, self.text_01.numero_ocurrencias))
        else:
            self.bus_reem_num_results.set('~ {} ~'.format('Sin resultados'))

    def _reemplazar_todo(self, event=None):
        self.text_01.reemplazar(self.entr_str_reempl.get(), True)
        if self.text_01.ocurrencias_encontradas:
            self.bus_reem_num_results.set('~ {} de {} ~'.format(self.text_01.numero_ocurrencia_actual, self.text_01.numero_ocurrencias))
        else:
            self.bus_reem_num_results.set('~ {} ~'.format('Sin resultados'))




if __name__ == '__main__':
    MainApp().mainloop()
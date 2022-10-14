from tkinter import *
from tkinter import ttk
from ScrollableNotebook import *
from extracion import Extracion
import json
import os

idOpenTab = 0

# Lista de clientes 
list_client = [
    "AFB",
    "ASISA"
]

#Carga mi usuario y la ruta de los ficheros
mypath = os.path.expanduser("~/")
path_modulo = mypath+"Compliance/file/desviaciones_{}.json"

class Aplicacion():
    
    def __init__(self):
        self.root = Tk()
        self.root.title("Example")
        
        '''
        crear la pestañas desde otro fichero .py
        '''
        self.notebook = ScrollableNotebook(
            self.root, 
            wheelscroll=True, 
            tabmenu=True,
            application=self,
        )
        
        '''Creamos la primera pestaña'''

        frame1 = Frame(self.notebook)
        self.notebook.add(frame1, text="WorkSpace")
        self.notebook.pack(fill="both", expand=True)
        self.notebook.bind_all("<<NotebookTabChanged>>",lambda e:self.alCambiar_Pestaña(e))
        text = Text(frame1)
        text.pack()
        Label(frame1, text="Pantalla PRINCIPAL").pack()
        
        ''' Crear boton para crear pestañas de EXTRACION'''
        Button(frame1,
               text="Issues EXTRACIONES",
               command=self.abrir_issuesExtracion,
               ).pack()

        ''' Crear boton para crear pestañas de DESVIACION'''

        Button(frame1,
               text="Issues DESVIACIONES",
               command=self.abrir_issuesDesviacion,
               ).pack()

    ''' FUNCION PARA ABRIR EXTRACION '''

    def abrir_issuesExtracion(self):
        print("aqui extracion")
        self.extracion = Extracion(self.notebook, application=self)
        self.notebook.add(self.extracion, text="Issues EXTRACIONES")

    ''' FUNCION PARA ABRIR DESVIACION '''

    def abrir_issuesDesviacion(self):
        global desviacion
        print("aqui desviacion")
        desviacion = Desviacion(self.notebook)
        self.notebook.add(desviacion, text="Issues DESVIACIONES")

    ''' FUNCION DONDE QUIERO QUE ME DESMARQUE EL TAG SELECIONADO DEL LIST BOX '''

    def alCambiar_Pestaña(self, event):
        #global idOpenTab
        #idOpenTab = event.widget.index('current')
        #tab = event.widget.tab(idOpenTab)['text']
        #print("ID : {}, TEXT : {}".format(idOpenTab,tab))
        #print(desviacion.DESVfr1_listbox)
        #desviacion.btn_nav_des.invoke()
        desviacion.bind('<FocusOut>', lambda e: desviacion.DESVfr1_listbox.selection_clear(0, END))

    def cerrar_ventana(self):
        self.notebook.forget(idOpenTab)
        self.notebook.notebookContent.forget(idOpenTab)

    def mainloop(self):
        self.root.mainloop()
class Desviacion(ttk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args)
        self.widgets()
    
    def widgets(self):

        ''' BUTTON PARA CERRAR PESTAÑA '''
        self.btn_nav = Button(
            self,
            text="CERRAR PESTAÑA",
            background="#39A2DB",
            border=0,
            borderwidth=0,
            highlightthickness=0,
            relief='flat',
            command=app.cerrar_ventana
        )
        self.btn_nav.grid(row=0, column=0, sticky="e")
        
        
        ''' OPTION MENU PARA ELEGIR EL CLIENTE'''
        
        self.clientesVar = tk.StringVar(self)
        self.clientesVar.set('CLIENTES')
        self.DESVfr1_optMn = tk.OptionMenu(
            self, 
            self.clientesVar, 
            *list_client, 
            command=self.cargar_Modulos,
        )
        self.DESVfr1_optMn.config(
            background = "#5F939A",
            foreground = "#F2EDD7",
            font=('Source Sans Pro',15,font.BOLD),
            activebackground="#3A6351",
            activeforeground="#F6D167",
            relief="groove",
            borderwidth=2,
            width=20
        )
        self.DESVfr1_optMn["menu"].config(
            background='#3A6351',
            selectcolor='red',
            activebackground='#5F939A',
            foreground="#F2EDD7",
            font=('Consolas', 13, font.BOLD),
        )
        self.DESVfr1_optMn.grid(row=1, column=0, padx=5, pady=5, sticky='new', columnspan=2)
        
        self.DESVlist_yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.DESVlist_xScroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.DESVfr1_listbox = tk.Listbox(
            self,
            xscrollcommand=self.DESVlist_xScroll.set, 
            yscrollcommand=self.DESVlist_yScroll.set,
            foreground='blue',
            selectbackground='#297F87',
            selectforeground='#F6D167',
            disabledforeground='black',
            exportselection=False,
            highlightbackground='gray88',
            highlightthickness=2,
            highlightcolor='#297F87',
            height=20,
            width=50
        )
        self.DESVfr1_listbox.grid(row=2, column=0, pady=(5,15), padx=(5,15), sticky='nsew')
        self.DESVlist_yScroll.grid(row=2, column=0, pady=(5,15), sticky='nse', columnspan=2)
        self.DESVlist_xScroll.grid(row=2, column=0, padx=5, sticky='sew', columnspan=2)
        self.DESVlist_xScroll['command'] = self.DESVfr1_listbox.xview
        self.DESVlist_yScroll['command'] = self.DESVfr1_listbox.yview

        self.btn_nav_des = Button(
            self,
            text="DESMARCAR",
            background="#39A2DB",
            border=0,
            borderwidth=0,
            highlightthickness=0,
            relief='flat',
            command=lambda x=self.DESVfr1_listbox : self.desmarcar(x)
        )
        self.btn_nav_des.grid(row=0, column=1, sticky="e")

    def desmarcar(self, event):
        print("desmarcar")
        event.selection_clear(0,END)
        
    ''' FUNCION QUE CARGA DESDE UN JSON, LOS MODULOS E INFORMACION DEL CLIENTE SELECIONADO'''
    def cargar_Modulos(self, clt_modulo=None, *args):
        if clt_modulo is not None:
            customer = clt_modulo
        ## --- LIMPIAR -----------------------------
        
        self.DESVfr1_listbox.delete(0,END)
        
        with open(path_modulo.format(customer)) as g:
            data = json.load(g)
            listModulo = []
            for md in data:
                listModulo.append(md['modulo'])

        listModulo.sort()

        self.DESVfr1_listbox.insert(END,*listModulo)

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()

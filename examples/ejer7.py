from tkinter import font
from tkinter import scrolledtext as st
import json
try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import *
    from PIL import Image, ImageTk
    from tkinter import messagebox as mb
except ImportError:
    import Tkinter as Tk
    import ttk
class Files(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgetsFiles()
    
        self.listServer.delete(0,END)
        self.srcRisk.delete('1.0',tk.END)
        self.srcImpact.delete('1.0',tk.END)
        self.cbxUser.delete(0,END)
    def cargar_files(self):
        #limpiando el arbol de vistas
        records = self.tree.get_children()
        for elemnt in records:
            self.tree.delete(elemnt)
        path_json = "/home/esy9d7l1/files.json"
        with open(path_json) as g:
                data = json.load(g)
                count = 0
                for md in data[clt]:
                    if count % 2 == 0:
                        self.tree.insert(parent='', index='end', iid=count, text='', value=(md['file'],md['owner'],md['gecos'],md['ownerGroup'],md['code']), tags=('evenrow'))
                    else:
                        self.tree.insert(parent='', index='end', iid=count, text='', value=(md['file'],md['owner'],md['gecos'],md['ownerGroup'],md['code']), tags=('oddrow'))
                    count += 1
    def selecionar_elemntFile(self, event):
        sel_valor = self.tree.focus()
        valor = self.tree.item(sel_valor, 'values')
        valFile = valor[0]
        path_json = "/home/esy9d7l1/files.json"
        with open(path_json) as g:
                data = json.load(g)
                for md in data[clt]:
                    if valFile == md['file']:
                        #limpiar------------------------------------                      
                        self.listServer.delete(0,END)
                        self.srcRisk.delete('1.0',tk.END)
                        self.srcImpact.delete('1.0',tk.END)
                        self.cbxUser.delete(0,END)
                        #-------------------------------------------
                        self.listServer.insert(END,*md['servers'])
                        self.srcRisk.insert(END,md['risk'])
                        self.srcImpact.insert(END,md['impact'])
                        self.cbxUser['values']=md["user"]
        self.cbxUser.set('CONTACTOS')
    def widgetsFiles(self):
        self.vtn_files = Toplevel(self)
        self.vtn_files.config(background='#F1ECC3')
        self.vtn_files.geometry("860x585+345+65")
        self.vtn_files.resizable(0,0)
        self.vtn_files.title('FILES')
        
        self.textBuscar = ttk.Entry(self.vtn_files,
                                        justify='left',
                                        width=40,
                                        font=('Trajan', 12))
        self.textBuscar.grid(row=0, column=0, padx=10, pady=10, ipady=7, sticky='we')

        self.btnBuscar = ttk.Button(self.vtn_files, 
                                        text='Buscar FICHERO')
        self.btnBuscar.grid(row=0, column=1, pady=10, sticky='w')

        self.btnCerrar = ttk.Button(self.vtn_files, 
                                        text='Cerrar')
        self.btnCerrar.grid(row=0, column=2, padx=60, pady=10, sticky=E)

        self.labelframe1=ttk.LabelFrame(self.vtn_files, text="DATOS")
        self.labelframe1.grid(column=0, row=1, padx=10, pady=10, columnspan=3, sticky='nsew')
        self.tree_scrollbar=tk.Scrollbar(self.labelframe1, orient=tk.VERTICAL)
        self.tree_scrollbar.grid(column=1, row=0, sticky=N+S, pady=10)
        #creamos el treeview
        self.tree = ttk.Treeview(self.labelframe1, 
                                yscrollcommand=self.tree_scrollbar.set,
                                height=9)
        #configuramos el scroll al trieview
        self.tree_scrollbar.config(command=self.tree.yview)
        #creamos las columnas
        self.tree['columns'] = ("FILE","ACCOUNT","GECOS","OWNERGROUP","CODE")
        #formato a las columnas
        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column("FILE", anchor=W, width=140)
        self.tree.column("ACCOUNT", anchor=CENTER, width=200)
        self.tree.column("GECOS", anchor=CENTER, width=140)
        self.tree.column("OWNERGROUP", anchor=CENTER, width=200)
        self.tree.column("CODE", anchor=CENTER, width=140)
        #indicar cabecera
        self.tree.heading("#0", text="", anchor=W)
        self.tree.heading("#1", text="FILE", anchor=W)
        self.tree.heading("#2", text="ACCOUNT", anchor=CENTER)
        self.tree.heading("#3", text="GECOS", anchor=CENTER)
        self.tree.heading("#4", text="OWNER GROUP", anchor=CENTER)
        self.tree.heading("#5", text="CODE", anchor=CENTER)

        self.tree.tag_configure('oddrow', background="light cyan", font=('Trajan', 12))
        self.tree.tag_configure('evenrow', background="LightCyan3", font=('Trajan', 12))
        self.tree.grid(column=0, row=0, pady=10)

        self.labelframe2=ttk.LabelFrame(self.vtn_files, text="OTROS DATOS")
        self.labelframe2.grid(column=0, row=2, padx=10, pady=10, columnspan=3, sticky='nsew')
        
        self.lbl1 = ttk.Label(self.labelframe2, text='SERVER')
        self.lbl1.grid(row=0, column=0, pady=5, padx=5)

        self.listServer = tk.Listbox(self.labelframe2, height=3)
        self.fr2_scroll1 = tk.Scrollbar(self.labelframe2, orient=tk.VERTICAL)
        self.listServer.config(foreground='blue',
                                    selectforeground='white', 
                                    selectbackground='#347083', 
                                    font=('Trajan', 12),
                                    height=8, width=20,
                                    yscrollcommand=self.fr2_scroll1.set)
        self.fr2_scroll1.config(command=self.listServer.yview)
        self.listServer.grid(column=0, row=1, padx=5, pady=5, sticky=N+E+S+W, rowspan=2)
        self.fr2_scroll1.grid(column=0, row=1, sticky='nse', pady=5, rowspan=2)

        self.lbl2 = ttk.Label(self.labelframe2, text='RISK')
        self.lbl2.grid(row=0, column=1, pady=5, padx=10, sticky='W')
        
        self.btnCpRisk = ttk.Button(self.labelframe2, 
                                        text='Copiar')
        self.btnCpRisk.grid(row=0, column=1, padx=10, pady=10, sticky=E)
        
        self.srcRisk = st.ScrolledText(self.labelframe2,
                                    wrap=tk.WORD,
                                    highlightcolor='#548CA8',
                                    borderwidth=0, 
                                    highlightthickness=3,)
        self.srcRisk.config(font=('Trajan', 12), 
                                    width=27,
                                    height=4,
                                    foreground='#334257', 
                                    selectforeground='#EEEEEE', 
                                    selectbackground='#476072')
        self.srcRisk.grid(row=1, column=1, pady=5, padx=10, sticky='n')

        self.lbl3 = ttk.Label(self.labelframe2, text='IMPACT')
        self.lbl3.grid(row=0, column=2, pady=10, padx=5, sticky='W')

        self.btnCpImp = ttk.Button(self.labelframe2, 
                                        text='Copiar')
        self.btnCpImp.grid(row=0, column=2, padx=5, pady=10, sticky=E)

        self.srcImpact = st.ScrolledText(self.labelframe2,
                                    wrap=tk.WORD,
                                    highlightcolor='#548CA8',
                                    borderwidth=0, 
                                    highlightthickness=3,)
        self.srcImpact.config(font=('Trajan', 12), 
                                    width=27,
                                    height=4,
                                    foreground='#334257', 
                                    selectforeground='#EEEEEE', 
                                    selectbackground='#476072')
        self.srcImpact.grid(row=1, column=2, pady=5, padx=5, sticky='n')
        self.cbxUser = ttk.Combobox(self.labelframe2, foreground='blue', width=14)
        self.cbxUser.config(font=('Trajan', 12), justify='center')
        self.cbxUser.set('CONTACTO')
        self.cbxUser.grid(column=1, row=2, pady=10, padx=10, sticky='nsew')
        self.tree.bind("<ButtonRelease-1>", self.selecionar_elemntFile)
        self.cargar_files()
class Desviacion(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.columnconfigure(2, weight=5)
        self.rowconfigure(0, weight=1)
        self.frame1=ttk.LabelFrame(self, 
                                        text="CLIENTE / MODULO", 
                                        border=1, 
                                        relief='sunken')
        self.frame1.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
        global list_client
        list_client = ['',
                    'AFB',
                    'LBK',
                    ]            
        self.clientesVar1 = tk.StringVar(self)
        self.clientesVar1.set('CLIENTES')
        self.fr1_optMn = ttk.OptionMenu(self.frame1, 
                                            self.clientesVar1, 
                                            *list_client,
                                            command=self.cargar_modulo)
        self.fr1_optMn.config(width=25)
        self.fr1_optMn["menu"].config(background='#EEC4C4',
                                            selectcolor='gray2',
                                            activebackground='#F29191',
                                            foreground="gray3",
                                            font=('Trajan', 12))
        self.fr1_optMn.grid(row=0, column=0, padx=5, pady=5, columnspan=2, sticky='ew')
        self.fr1_btn = ttk.Button(self.frame1, text='Abrir', command=self.abrir_file)
        self.fr1_btn.grid(row=1,column=0)
    def abrir_file(self):
        global files
        files = Files(self)
    def callback(*args):
        id_tab = app.cuaderno.index(app.cuaderno.select())
        app.cuaderno.tab(id_tab, text='DESVIACIONES : '+clt)
    def cargar_modulo(self, *args):
        global clt
        clt = self.clientesVar1.get()
        print('cliente al cargar modulo : ',clt)
        self.callback(clt)
class ButtonNotebook(ttk.Notebook):
    _initialized = False
    def __init__(self, parent, *args, **kwargs):
        if not self._initialized:
            self._initialize()
            self._inititialized = True
        kwargs["style"] = "ButtonNotebook"
        super().__init__(*args, **kwargs)
        self._active = None
        self.bind("<ButtonPress-1>", self.on_tab_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_tab_close_release)
    def on_tab_close_press(self, event):
        name = self.identify(event.x, event.y)
        if name == "tab_btn_close":
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
    def on_tab_close_release(self, event):
        if not self.instate(['pressed']):
            return None
        name =  self.identify(event.x, event.y)
        if name == "tab_btn_close":
            index = self.index("@%d,%d" % (event.x, event.y))
            if index != 0:
                if self._active == index:
                    self.forget(index)
                    self.event_generate("<<NotebookTabClosed>>")
        self.state(["!pressed"])
        self._active = None
    def _initialize(self):
        self.style = ttk.Style()
        self.style.configure(".",
            font=('Trajan', 12, font.BOLD)
        )
        self.images = (
            tk.PhotoImage("im1", data='''
                          R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2f///////////////yH5
                          BAEKAAIALAAAAAAIAAgAAAMUCCAsCmO5OBVl8OKhoV3e9jQOkAAAOw==
                           '''),
            tk.PhotoImage("im2", data='''
                          R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2f///////////////yH5
                          BAEKAAMALAAAAAAIAAgAAAMPCDA8+gw+GGlVbWKqmwMJADs=
                          ''' ),
            tk.PhotoImage("im3", data='''
                          R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2f///////////////yH5B
                          AEKAAMALAAAAAAIAAgAAAMPGDE8+gw+GGlVbWKqmwsJADs=
                          ''')
        )
        self.style.element_create("tab_btn_close", "image", "im1",
                            ("active", "pressed", "!disabled", "im2"),
                            ("active", "!disabled", "im3"), border=8, sticky='')
        self.style.layout("ButtonNotebook", [("ButtonNotebook.client", {"sticky": "nswe"})])
        self.style.layout("ButtonNotebook.Tab", [
            ("ButtonNotebook.tab", {
                "sticky": "nswe", 
                "children": [
                    ("ButtonNotebook.padding", {
                        "side": "top", 
                        "sticky": "nswe",
                        "children": [
                            ("ButtonNotebook.focus", {
                                "side": "top", 
                                "sticky": "nswe",
                                "children": [
                                    ("ButtonNotebook.label", {"side": "left", "sticky": ''}),
                                    ("ButtonNotebook.tab_btn_close", {"side": "left", "sticky": ''}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])
        self.style.configure("ButtonNotebook.Tab",
            background='#FFE6E6',
            padding=[20, 10], 
        )         
        self.style.map('ButtonNotebook.Tab', background = [("selected", "#C70039"),
                                                      ("active", "#fc9292")],
                                        foreground = [("selected", "#ffffff"),
                                                      ("active", "#000000")]
                 ) 
class Aplicacion():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CONTINOUS COMPLIANCE")
        self.cuaderno = ButtonNotebook(self.root)
        self.contenedor = tk.Frame(self.cuaderno, 
                                    background='#f1ecc3',
                                    border=0,)
        self.contenedor.columnconfigure(0, weight=1)
        self.contenedor.columnconfigure(1, weight=1)
        self.contenedor.rowconfigure(0, weight=1)
        self.contenedor.rowconfigure(1, weight=1)
        self.cuaderno.add(self.contenedor, text='WorkSpace')
        self.cuaderno.pack(expand=1, fill='both')
        self.widgets_app()
    def abrir_issuesDesviacion(self):
        global desviacion
        desviacion = Desviacion(self)
        self.cuaderno.add(desviacion, text='Issues DESVIACIONES')
        self.cuaderno.select(desviacion)
    def widgets_app(self):
        self.btn1 = ttk.Button(self.contenedor, text='DESVIACIONES',
                                    compound='top',
                                    width=20,
                                    style='WS.TButton',
                                    command=self.abrir_issuesDesviacion)
        self.btn1.grid(padx=30, pady=30, row=0, column=0, ipady=40, sticky='wn')
    def mainloop(self):
        self.root.mainloop()
if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
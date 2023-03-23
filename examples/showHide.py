import tkinter as tk
from tkinter import scrolledtext as st
from tkinter import ttk

on = 1
_estado_actual = False

class Extracion(tk.Frame):
    def __init__(self, parent, app, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args)
        self.app = app
        self.create_frame()
        self.bind_all('<Control-l>', lambda e : self.close_frame(e))
        self.bind_all('<Control-f>', lambda e : self.searchPanel(e))


    def close_frame(self, event):
        global on
        if on:
            self.frame1.pack_forget()
            on = 0
        else:
            self.frame.pack_forget()
            self.frame1.pack_forget()
            self.frame2.pack_forget()
            self.create_frame()
            
            on = 1

    def create_frame(self):
        self.frame = tk.Frame(self, background="#F4F4F4")
        self.frame.pack(expand=1, fill=tk.BOTH)
        
        self.frame2 = tk.Frame(self.frame)
        self.frame2.pack(side="right", expand=True, fill=tk.BOTH)
        
        self.txt = st.ScrolledText(
                self.frame2,
                font=("Helvetica", 12),
            )
        self.txt.pack(expand=1, fill=tk.BOTH)

        self.frame1 = tk.Frame(self.frame, background='cyan')
        self.frame1.pack(expand=1, fill=tk.BOTH)
        
        self.btn_close = tk.Button(
            self.frame1,
            background="gold",
            text="Hide"
        )
        self.btn_close.pack(expand=0, anchor='ne')
        
        self.treeview = ttk.Treeview(
            self.frame1,
        )
        self.treeview.heading("#0", text="FICHEROS de EXTRACIONES", anchor="center")
        self.treeview.pack(fill='both', expand=True, ipadx=50)
        
        self.max = tk.Button(
            self.frame1,
            width=4,
            text="+",
            background="gold"
        )
        self.max.pack(side="right", expand=0)

        self.min = tk.Button(
            self.frame1,
            width=4,
            text="-",
            background="gold"
        )
        self.min.pack(side="left", expand=0)

    def searchPanel(self, event=None):
        global _estado_actual
        if not _estado_actual:
            self.busca_top = tk.Toplevel(self.frame1)
            self._w = 0
            self._y = 0
            window_width = 680
            window_height = 100
            bus_reem_top_msg_w = 240
            self.busca_top.overrideredirect(True)
            screen_width = (self.app.root.winfo_x() + 640)
            screen_height = (self.app.root.winfo_y()+40)
            position_top = int(screen_height)
            position_right = int(screen_width)
            self.busca_top.geometry(
                f'{window_width}x{window_height}+{position_right}+{position_top}')
            
            self.busca_top.config(
                bg="cyan", 
                padx=5, 
                pady=5
            )

            self.busca_frm_tit = tk.Frame(
                self.busca_top,
            )
            self.busca_frm_tit.pack(fill='x', expand=1)

            self.busca_frm_content = tk.Frame(
                self.busca_top,
                bg="silver",
                padx=5,
                pady=10
            )
            self.busca_frm_content.pack(fill='x', expand=1)

            self.busca_top.title('Buscar')
            self.bus_reem_num_results = tk.StringVar()
            self.bus_reem_num_results.set('~ {} ~'.format('No hay resultados'))

            self.buscar_01_msg = tk.Message(
                self.busca_frm_tit,
                textvariable=self.bus_reem_num_results,
                padx=10,
                pady=0
            )
            self.buscar_01_msg.pack(fill='both', expand=1)
            self.buscar_01_msg.config(
                width=bus_reem_top_msg_w,
                foreground="black",
                justify='center',
                font=("Helvetica", 14, 'bold')
            )

            self.var_entry_bsc = tk.StringVar(self)
            
            self.entr_str = tk.Entry(
                self.busca_frm_content,
                textvariable=self.var_entry_bsc,
            )
            self.entr_str.grid(row=0, column=0, padx=5, sticky="nsew")

            self.btn_cerrar_buscar = tk.Button(
                self.busca_frm_content,
                text='X',
            )
            self.btn_cerrar_buscar.grid(row=0, column=4, padx=5, pady=5)

            self.btn_limpiar = tk.Button(
                self.busca_frm_content,
                text='<<',
            )

            self.btn_limpiar.grid(
                row=0, column=1, padx=(5, 0), pady=5, sticky="nsew")

            self.btn_buscar_prev = tk.Button(
                self.busca_frm_content,
                text='<|',
            )

            self.btn_buscar_prev.grid(
                row=0, column=2, padx=(5, 0), pady=5, sticky="nsew")

            self.btn_buscar_next = tk.Button(
                self.busca_frm_content,
                text='|>',
            )

            self.btn_buscar_next.grid(
                row=0, column=3, padx=(5, 0), pady=5, sticky="nsew")

            self.entr_str.focus_set()

            _estado_actual = True
        else:
            _estado_actual = True
            return 'break'
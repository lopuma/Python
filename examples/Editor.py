import tkinter as tk
import tkinter.font as tkFont


class MyText(tk.Text):
    def __init__(self, parent=None, *args, **kwargs):
        tk.Text.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.bind("<Button-3><ButtonRelease-3>", self.mostrar_menu)

    def mostrar_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Ejecutar proceso", command=self.ejecutar_proceso)
        menu.tk.call("tk_popup", menu, event.x_root, event.y_root)

    # Genera un evento virtual que puede ser capturado desde otra parte de la app
    def ejecutar_proceso(self, event=None):
        self.event_generate("<<EXEP_Event>>")



class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.bind('<<EXEP_Event>>', self.ejecutar_proceso)


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


    def ejecutar_proceso(self, event=None):
        print("Ejecutando....")



if __name__ == "__main__":
    MainApp().mainloop()
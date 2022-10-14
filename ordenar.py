import pandas as pd
import tkinter as tk
from tkinter import ttk
def getTreeViewUser(df, frame):
    tv = ttk.Treeview(frame, columns=("#1", "#2", "#3", 
    "#4",'#5','#6','#7','#8','#9',
                                    "#10","#11","#12","#13","#14","#15","#16","#17","#18"))
    tv.heading('#0', text="Col0")
    tv.heading('#1', text="Col1")
    tv.heading('#2', text="Col2")
    tv.heading('#3', text="Col3")
    tv.heading('#4', text="Col4")
    tv.heading('#5', text="Col5")
    tv.heading('#6', text="Col6")
    tv.heading('#7', text="Col7")
    tv.heading('#8', text="Col8")
    tv.heading('#9', text="Col9")
    tv.heading('#10', text="Col10")
    tv.heading('#11', text="Col11")
    tv.heading('#12', text="Col12")
    tv.heading('#13', text="Col13")
    tv.heading('#14', text="Col14")
    tv.heading('#15', text="Col15")
    tv.heading('#16', text="Col16")
    tv.heading('#17', text="Col17")
    tv.heading('#18', text="Col18")


    for ind in df.index:
    #        rojo = df.values[ind][17]
    #        tag=""
    #        if(rojo==1):
    #            tag="col18"

        tv.insert("", tk.END, text=ind+1,
                        values=(df.values[ind][0],df.values[ind][1],
                                df.values[ind][2],df.values[ind][3],
                                df.values[ind][4],df.values[ind][5],
                                df.values[ind][6],df.values[ind][7],
                                df.values[ind][8],df.values[ind][9],
                                df.values[ind][10],df.values[ind][11],
                                df.values[ind][12],df.values[ind][13],
                                df.values[ind][14],df.values[ind][15],
                                df.values[ind][16],
                                df.values[ind][17]))

    #    tv.tag_configure('rojo', background='#F6CECE')

    scrollbar_vertical = ttk.Scrollbar(frame, orient='vertical', command = tv.yview)
    scrollbar_vertical.pack(side='right', fill=tk.Y)

    scrollbar_horizontal = ttk.Scrollbar(frame, orient='horizontal', command = tv.xview)
    scrollbar_horizontal.pack(side='bottom', fill=tk.X)

    tv.configure(yscrollcommand=scrollbar_vertical.set)
    tv.configure(xscrollcommand=scrollbar_horizontal.set)


    return tv

def clickbutton():
    file = pd.read_excel('/home/esy9d7l1/Alvaro/Desarrollo/Python/Untitled.xlsx')
    df = pd.DataFrame(file)
    getTreeViewUser(df, main_window).pack(expand=True, fill='both')

class Application(ttk.Frame):
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.geometry("600x500")
        self.button = tk.Button(main_window, text="Button", command=clickbutton).pack()
        self.progressbar = ttk.Progressbar(main_window)
        self.progressbar.pack()

main_window = tk.Tk()
app = Application(main_window)
app.mainloop()
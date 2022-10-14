import tkinter as tk
last_y= None
root = tk.Tk()
Text_widget= tk.Text(root, height=20, width=30)
Text_widget.pack()
Text_widget.insert(tk.END, "t\nh\ni\ns\n \na\n \nt\ne\ns\nt\n \nt\no\n \nf\ni\ng\nu\nr\ne\n \nt\nh\ni\ns\n \no\nu\nt\n\
    t\nh\ni\ns\n \na\n \nt\ne\ns\nt\n \nt\no\n \nf\ni\ng\nu\nr\ne\n \nt\nh\ni\ns\n \no\nu\nt\n\
    t\nh\ni\ns\n \na\n \nt\ne\ns\nt\n \nt\no\n \nf\ni\ng\nu\nr\ne\n \nt\nh\ni\ns\n \no\nu\nt\n\
    t\nh\ni\ns\n \na\n \nt\ne\ns\nt\n \nt\no\n \nf\ni\ng\nu\nr\ne\n \nt\nh\ni\ns\n \no\nu\nt\n\
    t\nh\ni\ns\n \na\n \nt\ne\ns\nt\n \nt\no\n \nf\ni\ng\nu\nr\ne\n \nt\nh\ni\ns\n \no\nu\nt\n")
Text_widget.config(state='disabled')
def tablet_drag_y(event):
    global last_y
    print("5")
    if last_y==None:
        last_y=event.y_root
        event.widget.tag_remove(tk.SEL, "1.0", tk.END)
        return "break"
    movement= (event.y_root-last_y)
    event.widget.yview(tk.SCROLL,-1*(movement), "pixels")
    last_y=event.y_root
    event.widget.tag_remove(tk.SEL, "1.0", tk.END)
    return "break"
def cancel_normal_scroll(event):
    return "break"
Text_widget.bind("<B1-Motion>", tablet_drag_y)
Text_widget.bind("<Enter>", cancel_normal_scroll)
Text_widget.bind("<Leave>", cancel_normal_scroll)
tk.mainloop()
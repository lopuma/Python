from tkinter import *
from tkinter import messagebox
root = Tk()
root.attributes('-fullscreen', True)
root.configure(background='white')
scrW = root.winfo_screenwidth()
scrH = root.winfo_screenheight()  
workwindow = str(1024) + "x" + str(768)+ "+" +str(int((scrW-1024)/2)) + "+" +str(int((scrH-768)/2))
top1 = Toplevel(root, bg="light blue")
top1.geometry(workwindow)
top1.title("Top 1 - Workwindow")
top1.attributes("-topmost", 1)  # make sure top1 is on top to start
root.update()                   # but don't leave it locked in place
top1.attributes("-topmost", 0)  # in case you use lower or lift
#exit button - note: uses grid
b3=Button(root, text="Egress", command=root.destroy)
b3.grid(row=0,column=0,ipadx=10, ipady=10, pady=5, padx=5, sticky = W+N)
#____________________________
root.withdraw()
mb1=messagebox.askquestion(top1, "Pay attention: \nThis is the message?")
messagebox.showinfo("Say Hello", "Hello World")
root.deiconify()
top1.lift(aboveThis=None)
#____________________________
root.mainloop()
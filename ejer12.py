import tkinter

app = tkinter.Tk()
app.geometry("300x200")
app.title("TkinterCustomButton")

def button_function():
    print("Button pressed")

button_1 = tkinter.Button(text="My Button",  command=button_function)
button_1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

app.mainloop()
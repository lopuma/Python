from tkinter import *
class ButtonHandler:
    def __init__(self):     
        self.root = Tk()
        self.root.geometry('600x500+200+200')
        self.mousedown = False
        self.label = Label(self.root, text=str(self.mousedown))
        self.can = Canvas(self.root, width='500', height='400', bg='white')
        self.can.bind("<Motion>",lambda x:self.handler(x,'motion'))
        self.can.bind("<Button-1>",lambda x:self.handler(x,'press'))
        self.can.bind("<ButtonRelease-1>",lambda x:self.handler(x,'release'))
        self.label.pack()
        self.can.pack()
        self.root.mainloop()
    def handler(self,event,button_event):
        print('Handler %s' % button_event)
        if button_event == 'press':
            self.mousedown = True
        elif button_event == 'release':
            self.mousedown = False
        elif button_event == 'motion':
            if self.mousedown:              
                r = 5
                self.can.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill="orange")
        self.label.config(text=str(self.mousedown))
button_event = ButtonHandler()
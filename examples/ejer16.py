import win32con
import win32api
import win32gui
import tkinter as tk
def override(event):
    hwnd = win32gui.GetParent(root.winfo_id())
    style= win32api.GetWindowLong(hwnd, win32con.GWL_STYLE)
    style&= ~win32con.WS_MINIMIZEBOX
    style&= ~win32con.WS_MAXIMIZEBOX
    style&= ~win32con.WS_SYSMENU
    style&= ~win32con.WS_CAPTION
    #style&= ~win32con.WS_SIZEBOX
    valid= win32api.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
    root.bind('<Map>', None)
root = tk.Tk()
root.bind('<Map>', override)
root.mainloop()

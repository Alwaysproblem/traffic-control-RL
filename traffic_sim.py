import numpy as np
import time
import sys

if sys.version_info.major==2:
    import Tkinter as tk
else:
    import tkinter as tk


class traffic_lights(tk.Tk,object):
    def __init__(self):
        super(traffic_lights, self).__init__()
        self.title('traffic_lights')
        self.geometry("500x500")
        self.build_menu()
        self.Cross_street()

    def Exit(self):
        self.destroy()

    def build_menu(self):
        self.menubar=tk.Menu(self)

        self.filemenu=tk.Menu(self.menubar,tearoff=0)
        self.filemenu.add_command(label="Start",command=self.Exit)
        self.filemenu.add_command(label="Pause",command=self.Exit)
        self.filemenu.add_command(label="Exit",command=self.Exit)
        self.menubar.add_cascade(label="Menu",menu=self.filemenu)

        self.setmenu = tk.Menu(self.menubar,tearoff=0)
        self.setmenu.add_command(label="Set",command=self.Exit)
        self.menubar.add_cascade(label="Control",menu=self.setmenu)
        self.config(menu=self.menubar)
    
    def Cross_street(self):
        self.canvas=tk.Canvas(self,bg="white",height=500,width=500)
        self.canvas.create_line(0,200,200,200)
        self.canvas.create_line(200,0,200,200)
        self.canvas.create_line(0,300,200,300)
        self.canvas.create_line(300,0,300,200)
        self.canvas.create_line(200,500,200,300)
        self.canvas.create_line(500,200,300,200)
        self.canvas.create_line(300,500,300,300)
        self.canvas.create_line(500,300,300,300)
        self.canvas.pack()


if __name__ == '__main__':
    env = traffic_lights()
    env.mainloop()

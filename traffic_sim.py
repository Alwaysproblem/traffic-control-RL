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

    def build_set_menu(self):
        j=1
        speed=['5','10','15','20','25']
        self.Set=tk.Toplevel()
        self.Set.title('Set')
        self.Set.geometry('400x300')

        self.Set.menubutton_1=tk.Menubutton(self.Set,text='speed')
        self.Set.menubutton_1.menu=tk.Menu(self.Set.menubutton_1)
        self.Set.menubutton_1.pack()

        self.Set.user_choice = tk.IntVar()
        self.Set.user_choice.set(1)
        self.Set.file_menu=tk.Menu(self.Set.menubutton_1,tearoff=0)
        for i in speed :
            self.Set.file_menu.add_radiobutton(label=i,variable=self.Set.user_choice,value=j)
            j+=1
        self.Set.menubutton_1.config(menu=self.Set.file_menu)

    def build_menu(self):
        self.menubar=tk.Menu(self)

        self.filemenu=tk.Menu(self.menubar,tearoff=0)
        self.filemenu.add_command(label="Start",command=self.Exit)
        self.filemenu.add_command(label="Pause",command=self.Exit)
        self.filemenu.add_command(label="Exit",command=self.Exit)
        self.menubar.add_cascade(label="Menu",menu=self.filemenu)

        self.setmenu = tk.Menu(self.menubar,tearoff=0)
        self.setmenu.add_command(label="Set",command=self.build_set_menu)
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

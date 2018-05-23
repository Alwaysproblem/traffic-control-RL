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
        self.Car()
        self.canvas.pack()
        self.move_car()

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
        self.canvas.create_line(0,225,225,225)
        self.canvas.create_line(225,0,225,225)
        self.canvas.create_line(0,275,225,275)
        self.canvas.create_line(275,0,275,225)
        self.canvas.create_line(225,500,225,275)
        self.canvas.create_line(500,225,275,225)
        self.canvas.create_line(275,500,275,275)
        self.canvas.create_line(500,275,275,275)

    def Car(self):
        self.x1=245
        self.x2=255
        self.y1=0
        self.y2=10
        self.x3=0
        self.x4=10
        self.y3=245
        self.y4=255
        self.Car_1 = self.canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill='black')

    def move_car(self):
        for self.vector in range(0,20):
            self.canvas.coords(self.Car_1,(self.x1,self.y1,self.x2,self.y2))
            self.canvas.coords(self.Car_2,(self.x3,self.y3,self.x4,self.y4))
            self.update()
            self.y1+=25
            self.y2+=25
            self.x3+=25
            self.x4+=25
            time.sleep(0.5) 

    

if __name__ == '__main__':
    env = traffic_lights()
    env.mainloop()

import numpy as np
import time
import sys
import random

if sys.version_info.major==2:
    import Tkinter as tk
else:
    import tkinter as tk


class traffic_lights(tk.Tk,object):
    def __init__(self):
        super(traffic_lights, self).__init__()
        self.change=1
        self.title('traffic_lights')
        self.geometry("500x500")
        self.build_menu()
        self.Cross_street()
        self.lights()
        self.canvas.pack()

    def Exit(self):
        self.destroy()

    def build_set_menu(self):
        j=1
        speed=['10','20','30','40']
        self.Set=tk.Toplevel()
        self.Set.title('Set')
        self.Set.geometry('400x300')

        self.Set.menubutton_1=tk.Menubutton(self.Set,text='speed',relief='raised')
        self.Set.menubutton_1.menu=tk.Menu(self.Set.menubutton_1)
        self.Set.menubutton_1.pack()

        self.Set.user_choice = tk.IntVar()
 
        self.Set.file_menu=tk.Menu(self.Set.menubutton_1,tearoff=0)
        for i in speed :
            self.S=self.Set.file_menu.add_radiobutton(label=i,variable=self.Set.user_choice,value=i,command=self.get_speed)
            j+=1
        self.Set.menubutton_1.config(menu=self.Set.file_menu)
    
    def get_speed(self):    #get the speed user require
        self.speed=self.Set.user_choice.get()


    def build_menu(self):
        self.menubar=tk.Menu(self)

        self.filemenu=tk.Menu(self.menubar,tearoff=0)
        self.filemenu.add_command(label="Start",command=self.Car)
        self.filemenu.add_command(label="Exit",command=self.Exit)
        self.menubar.add_cascade(label="Menu",menu=self.filemenu)

        self.setmenu = tk.Menu(self.menubar,tearoff=0)
        self.setmenu.add_command(label="Set",command=self.build_set_menu)
        self.menubar.add_cascade(label="Control",menu=self.setmenu)
        self.config(menu=self.menubar)
    
    def Cross_street(self):    # build the street
        self.canvas=tk.Canvas(self,bg="white",height=500,width=500)
        self.canvas.create_line(0,225,225,225)
        self.canvas.create_line(225,0,225,225)
        self.canvas.create_line(0,275,225,275)
        self.canvas.create_line(275,0,275,225)
        self.canvas.create_line(225,500,225,275)
        self.canvas.create_line(500,225,275,225)
        self.canvas.create_line(275,500,275,275)
        self.canvas.create_line(500,275,275,275)

    def lights(self):       # initial light and light color
        self.light_1=self.canvas.create_rectangle(235,225,265,215,fill='gray')
        self.light_2=self.canvas.create_rectangle(215,235,225,265,fill='gray')
        self.light_3=self.canvas.create_rectangle(275,235,285,265,fill='gray')
        self.light_1=self.canvas.create_rectangle(235,275,265,285,fill='gray')

        self.red_1=self.canvas.create_oval(235,225,245,215,fill='red')
        self.red_2=self.canvas.create_oval(215,255,225,265,fill='gray')
        self.red_3=self.canvas.create_oval(275,235,285,245,fill='gray')
        self.red_4=self.canvas.create_oval(255,275,265,285,fill='red')

        self.green_1=self.canvas.create_oval(255,225,265,215,fill='gray')
        self.green_2=self.canvas.create_oval(215,235,225,245,fill='green')
        self.green_3=self.canvas.create_oval(275,255,285,265,fill='green')
        self.green_4=self.canvas.create_oval(235,275,245,285,fill='gray')

    def light_change(self):     #change the color of lights
            if self.change ==1:
                self.canvas.itemconfig(self.green_1,fill = 'green')
                self.canvas.itemconfig(self.green_2,fill = 'gray')
                self.canvas.itemconfig(self.green_3,fill = 'gray')
                self.canvas.itemconfig(self.green_4,fill = 'green')

                self.canvas.itemconfig(self.red_1,fill = 'gray')
                self.canvas.itemconfig(self.red_2,fill = 'red')
                self.canvas.itemconfig(self.red_3,fill = 'red')
                self.canvas.itemconfig(self.red_4,fill = 'gray')
                self.change =0
            else:
                self.canvas.itemconfig(self.green_1,fill = 'gray')
                self.canvas.itemconfig(self.green_2,fill = 'green')
                self.canvas.itemconfig(self.green_3,fill = 'green')
                self.canvas.itemconfig(self.green_4,fill = 'gray')

                self.canvas.itemconfig(self.red_1,fill = 'red')
                self.canvas.itemconfig(self.red_2,fill = 'gray')
                self.canvas.itemconfig(self.red_3,fill = 'gray')
                self.canvas.itemconfig(self.red_4,fill = 'red')
                self.change =1



    def Car(self):
        self.car=[]
        self.count=0
        self.speed=10  # initial speed 
        while(True):
            if self.car==[]:    # if there no car, then create cars in random direction
                if  random.random()>0.5:
                    self.car_1=create_car_up()
                    self.car1 = self.canvas.create_rectangle(self.car_1.x1,self.car_1.y1,self.car_1.x2,self.car_1.y2,fill='yellow')
                    self.car.append([self.car1,self.car_1])
                if  random.random()>0.5:
                    self.car_2=create_car_left()
                    self.car2 = self.canvas.create_rectangle(self.car_2.x1,self.car_2.y1,self.car_2.x2,self.car_2.y2,fill='blue')
                    self.car.append([self.car2,self.car_2])

            for i in self.car:              # loop, create car
                self.crash=0
                if (i[1].x1==245 and i[1].x2==255):      # the car from up
                    self.color_1 = self.canvas.itemcget(self.red_1, 'fill')
                    if (self.color_1=='red'and i[1].y1+self.speed>=215 and i[1].y1<=215): # if meat red light stop
                        i[1].y1+=0
                        i[1].y2+=0
                    else:
                        for j in self.car:
                            if (j!=i and j[1].x1==245 and j[1].x2==255):
                                if (i[1].y2+self.speed >j[1].y1 and i[1].y2<=j[1].y1):   # if it will have a crash with a other car stop
                                    self.crash=1
                                    break

                        if self.crash==0:   # if no crash at all, change its position
                            i[1].y1+=self.speed
                            i[1].y2+=self.speed
                            if(i[1].y2>=500):
                                self.canvas.coords(i[0],(i[1].x1,500,i[1].x2,i[1].y2))  # update car's location
                                self.canvas.delete(i)
                                self.car.remove(i)
                            else:
                                self.canvas.coords(i[0],(i[1].x1,i[1].y1,i[1].x2,i[1].y2))
                        else:
                            i[1].y1+=0
                            i[1].y2+=0


                if (i[1].y1==245  and i[1].y2==255):
                    self.color_2 = self.canvas.itemcget(self.red_2, 'fill')
                    if (self.color_2=="red"and i[1].x1+self.speed>=215 and i[1].x1<=215):
                        i[1].x1+=0
                        i[1].x2+=0
                        self.canvas.coords(i[0],(i[1].x1,i[1].y1,i[1].x2,i[1].y2))
                    else:
                        for j in self.car:
                            if (j!=i and j[1].y1==245 and j[1].y2==255):
                                if (i[1].x2+self.speed >j[1].x1 and i[1].x2<=j[1].x1):
                                    self.crash=1
                                    break

                        if self.crash==0:
                            i[1].x1+=self.speed
                            i[1].x2+=self.speed
                            if(i[1].x2>=500):
                                self.canvas.coords(i[0],(i[1].x1,500,i[1].x2,i[1].y2))
                                self.canvas.delete(i)
                                self.car.remove(i)
                            else:
                                self.canvas.coords(i[0],(i[1].x1,i[1].y1,i[1].x2,i[1].y2))
                        else:
                            i[1].x1+=0
                            i[1].x2+=0

            if (self.count % 3==0): # when it loop 3 times ,the cars start to be created
                if  random.random()>0.5:   # randomly create cars, 50%
                    self.car_1=create_car_up()
                    self.car1 = self.canvas.create_rectangle(self.car_1.x1,self.car_1.y1,self.car_1.x2,self.car_1.y2,fill='yellow')
                    self.car.append([self.car1,self.car_1])

            if(self.count % 2==0):
                if random.random()>0.5:
                    self.car_2=create_car_left()
                    self.car2 = self.canvas.create_rectangle(self.car_2.x1,self.car_2.y1,self.car_2.x2,self.car_2.y2,fill='blue')
                    self.car.append([self.car2,self.car_2])

            self.count+=1
            if (self.count % 24==0):
                self.light_change()
            self.update()
            time.sleep(0.25)  #system sleep 0.25
            

class create_car_up(object):
    def __init__(self):
        self.x1=245
        self.x2=255
        self.y1=0
        self.y2=10

class create_car_left(object):
    def __init__(self):
        self.x1=0
        self.x2=10
        self.y1=245
        self.y2=255

if __name__ == '__main__':
    env = traffic_lights()
    env.mainloop()

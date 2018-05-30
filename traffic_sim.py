from Car import Vehicle
from Light import light
from Point import point

import numpy as np
import time
import sys
import random


if sys.version_info.major==2:
    import Tkinter as tk
else:
    import tkinter as tk

class traffic(tk.Tk,object):
    def __init__(self):
        super(traffic, self).__init__()
        self.UNIT = 10
        self.change = True
        self.car_list = []
        # self.time_stamp = 0
        self.speed = self.UNIT  # initial speed 
        self.roadLen = 12 # self.UNIT
        self.size = 100
        self.canvas = tk.Canvas(self, bg = "white", height = self.size * self.UNIT, width = self.size * self.UNIT)
        roadV_light_size = (6, 2)
        roadH_light_size = (2, 6)

        self.road_point_NW = point(*((self.size/2 - self.roadLen/2),(self.size/2 - self.roadLen/2)))      # Northwest
        self.road_point_SW = point(*((self.size/2 - self.roadLen/2),(self.size/2 + self.roadLen/2)))       # Southwest
        self.road_point_NE = point(*((self.size/2 + self.roadLen/2),(self.size/2 - self.roadLen/2)))       # Northeast
        self.road_point_SE = point(*((self.size/2 + self.roadLen/2), (self.size/2 + self.roadLen/2)))       # southeast

        self.light_NW = light(
            point(self.road_point_NW.x - roadH_light_size[0], self.road_point_NW.y),
            *roadH_light_size,
            self.canvas,
            self.UNIT,
            'NW',
            'L'
        )
        self.light_SW = light(
            self.road_point_SW,
            *roadV_light_size,
            self.canvas,
            self.UNIT,
            'SW',
            'L'
            )
        self.light_SE = light(
            point(self.road_point_SE.x,self.size/2),
            *roadH_light_size,
            self.canvas,
            self.UNIT,
            'SE',
            'R'
            )
        self.light_NE = light(
            point(self.size/2, self.road_point_NE.y - roadV_light_size[1]),
            *roadV_light_size,
            self.canvas,
            self.UNIT,
            'NE',
            'R'
            )
        self.lightList = (self.light_NW, self.light_SW, self.light_SE, self.light_NE)
        self.car_l = Vehicle('left', self.lightList, self.canvas, self.UNIT, self.size, self.roadLen)
        self.car_r = Vehicle('right', self.lightList, self.canvas, self.UNIT, self.size, self.roadLen)
        self.car_u = Vehicle('up', self.lightList, self.canvas, self.UNIT, self.size, self.roadLen)
        self.car_d = Vehicle('down', self.lightList, self.canvas, self.UNIT, self.size, self.roadLen)

    def backgound(self):
        self.title('traffic_lights')
        self.geometry(f"{self.size * self.UNIT}x{self.size * self.UNIT}")
        self.build_menu()
        self.Cross_street()
        self.light()
        self.canvas.pack()

        car_list = [(self.car_l, 'l'), (self.car_r, 'r'), (self.car_u, 'u'), (self.car_d, 'd')]

        for _ in range(100):
            time.sleep(0.5)
            for i in car_list:
                i[0].move()
                print(f'carID: {i[1]}', end = '')
                i[0].show()

            self.canvas.update()
            print()

    def Exit(self):
        self.destroy()

    def build_set_menu(self):
        j=1
        speed=['10','20','30','40']
        self.Set=tk.Toplevel()
        self.Set.title('Set')
        self.Set.geometry('200x100')

        self.Set.menubutton_1=tk.Menubutton(self.Set,text='speed',relief='raised')
        self.Set.menubutton_1.menu=tk.Menu(self.Set.menubutton_1)
        self.Set.menubutton_1.pack()

        self.Set.user_choice = tk.IntVar()
 
        self.Set.file_menu=tk.Menu(self.Set.menubutton_1,tearoff=0)
        for i in speed :
            self.S=self.Set.file_menu.add_radiobutton(label=i,variable=self.Set.user_choice,value=i,command=self.get_speed)
            j += 1
        self.Set.menubutton_1.config(menu=self.Set.file_menu)
    
    def get_speed(self):    #get the speed user require
        self.speed=self.Set.user_choice.get() * self.UNIT

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
        # self.canvas=tk.Canvas(self,bg="white",height = self.size * self.UNIT, width = self.size * self.UNIT)
        self.canvas.create_rectangle(
            0,0, 
            self.road_point_NW.x * self.UNIT, self.road_point_NW.y * self.UNIT, 
            fill = 'black'
        )
        self.canvas.create_rectangle(
            0, self.road_point_SW.y * self.UNIT, 
            self.road_point_SW.x * self.UNIT, self.size * self.UNIT, 
            fill = 'black'
        )
        self.canvas.create_rectangle(
            self.road_point_SE.x * self.UNIT, self.road_point_SE.y * self.UNIT, 
            self.size * self.UNIT, self.size * self.UNIT, 
            fill = 'black'
        )
        self.canvas.create_rectangle(
            self.road_point_NE.x * self.UNIT, 0, 
            self.size * self.UNIT, self.road_point_NE.y * self.UNIT, 
            fill = 'black'
        )
        # create the line:
        line_col = 'orange'
        line_patten = (20, 20)
        line_wid = self.UNIT / 2
        self.canvas.create_line(
            0, self.size/2 * self.UNIT, 
            self.road_point_NW.x * self.UNIT, self.size/2 * self.UNIT, 
            fill = line_col, 
            dash = line_patten,
            width = line_wid
        )
        self.canvas.create_line(
            self.road_point_NE.x * self.UNIT, self.size/2 * self.UNIT, 
            self.size * self.UNIT, self.size/2 * self.UNIT, 
            fill = line_col,
            dash = line_patten,
            width = line_wid
        )
        self.canvas.create_line(
            self.size/2 * self.UNIT, 0,
            self.size/2 * self.UNIT, self.road_point_NE.y * self.UNIT,
            fill = line_col,
            dash = line_patten,
            width = line_wid
        )
        self.canvas.create_line(
            self.size/2 * self.UNIT, self.road_point_SE.y * self.UNIT,
            self.size/2 * self.UNIT, self.size * self.UNIT,
            fill = line_col,
            dash = line_patten,
            width = line_wid
        )

    def light(self):
        self.light_NW.draw()
        self.light_SW.draw()
        self.light_SE.draw()
        self.light_NE.draw()

    def light_change(self):     #change the color of lights
        pass
        # self.light_NW._Change('')
        # self.light_SW._Change('')
        # self.light_SE._Change('')
        # self.light_NE._Change('')


    def Car(self):
        pass

    def closestcar(self,car_list):
        origin_list = list(car_list)
        new_list = [car for car in origin_list if car.Dis_light >= 0]
        # for car in origin_list:
        #     if car.Dis_light >= 0:
        #         new_list.append(car)
        sorted(new_list,key = self.sortcar)
        # print(new_list)
        return new_list[0].Dis_light
    
    def sortcar(self,vehicle):
        return vehicle.Dis_light


class TrafficSimulator(traffic):
    def __init__(self):
        super(TrafficSimulator, self).__init__()
        self.action = ['switch', 'stay']
        self.n_action = len(self.action)
        self.time_stamp = 0
        self.backgound()

    def restart(self):
        pass

    def render(self):
        pass

    def step(self, action):
        pass




if __name__ == '__main__':
    # env = traffic_lights()
    # env.Cross_street()
    env = TrafficSimulator()
    env.mainloop()

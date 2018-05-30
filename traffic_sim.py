"""
    Two actions: decide to switch or not.

    Reward -1.0 if a car is stopped at a red light on either road, zero
    otherwise.

    Optimise discounted sum of future reward.

    Use discount factor: gamma = .9

    Use learning rate: alpha = .1

    Epsilon-greedy exploration 10%

    Plot and compare performance measures for both the fixed switching and
    learnt policies. 
"""

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
        roadV_light_size = (6, 2)  #(6 / 2, 2 / 2)
        roadH_light_size = (2, 6)  #(2 / 2, 6 / 2)

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
            'red',
            'L'
        )
        self.light_SW = light(
            self.road_point_SW,
            *roadV_light_size,
            self.canvas,
            self.UNIT,
            'SW',
            'green',
            'L'
            )
        self.light_SE = light(
            point(self.road_point_SE.x, self.size/2),
            *roadH_light_size,
            self.canvas,
            self.UNIT,
            'SE',
            'red',
            'R'
            )
        self.light_NE = light(
            point(self.size/2, self.road_point_NE.y - roadV_light_size[1]),
            *roadV_light_size,
            self.canvas,
            self.UNIT,
            'NE',
            'green',
            'R'
            )
        self.lightList = (self.light_NW, self.light_SW, self.light_SE, self.light_NE)
        self.car_l = Vehicle('left', self.lightList, self.canvas, self.UNIT, self.size, self.roadLen)
        self.car_r = Vehicle('right', self.lightList, self.canvas, self.UNIT, self.size, self.roadLen)
        self.car_u = Vehicle('up', self.lightList, self.canvas, self.UNIT, self.size, self.roadLen)
        self.car_d = Vehicle('down', self.lightList, self.canvas, self.UNIT, self.size, self.roadLen)

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
        self.filemenu.add_command(label = "Start",command = self.Car)
        self.filemenu.add_command(label = "Exit",command = self.Exit)
        self.menubar.add_cascade(label = "Menu",menu = self.filemenu)

        self.setmenu = tk.Menu(self.menubar,tearoff=0)
        self.setmenu.add_command(label = "Set", command = self.build_set_menu)
        self.menubar.add_cascade(label = "Control", menu = self.setmenu)
        self.config(menu = self.menubar)
    
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

    def backgound(self):
        self.title('traffic_lights')
        self.geometry(f"{self.size * self.UNIT}x{self.size * self.UNIT}")
        self.build_menu()
        self.Cross_street()
        self.light()
        self.canvas.pack()


        car_list = [(self.car_l, 'l'), (self.car_r, 'r'), (self.car_u, 'u'), (self.car_d, 'd')]

        for x in range(100):
            time.sleep(1)
            print(f"{x%3}")
            self.light_NW.Change()
            # self.light_SW._Change('green')
            # self.light_SE._Change('red')
            # self.light_NE._Change('green')

            # for i in car_list:
            #     # print(f'carID: {i[1]} ', end = '')
            #     # i[0].show()
            #     i[0].move()
            self.canvas.update()
        #     print()

    def _ClosestCar(self,car_list):
        """
        output:
        the closest car position
        the number of queueing car
        """
        def sortcar(vehicle):
            return vehicle.Dis_light

        origin_list = list(car_list)
        new_list = [car for car in origin_list if car.Dis_light >= 0]
        new_list.sort(key = sortcar)
        return new_list[0].Dis_light,len([car for car in new_list if car.moveState == False])
    
    def ClosestCar(self):
        return self._ClosestCar(self.car_list)

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
        self.canvas.update()
        time.sleep(0.5)
        # self.time_stamp += 1
        # if self.time_stamp >= 1000:
        #     self.Exit()

    def step(self, action):
        """
        output is like:
        observation, reward, done, info
        observation is like:
        [
            closest car pos for Road 1, # 0-8
            closest car pos for Road 2, # 0-8
            Road 1 light state, # 0 means red, 1 if light is green
            Road 2 light state, # 0 means red, 1 if light is green
            Light delay # 0-3
        ]
        reward -1.0 if a car is stopped at a red light on either road, zero otherwise.
        """
        pass




if __name__ == '__main__':
    # env = traffic_lights()
    # env.Cross_street()
    env = TrafficSimulator()
    env.mainloop()

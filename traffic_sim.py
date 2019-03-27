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
from QLearning import QL

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
        # self.car_l = Vehicle('left', self.lightList, self.canvas, self.UNIT, self.size, self.roadLen)
        # self.car_r = Vehicle('right', self.lightList, self.canvas, self.UNIT, self.size, self.roadLen)
        # self.car_u = Vehicle('up', self.lightList, self.canvas, self.UNIT, self.size, self.roadLen)
        # self.car_d = Vehicle('down', self.lightList, self.canvas, self.UNIT, self.size, self.roadLen)

    def Exit(self):
        self.destroy()

    def random_create_car(self):
        for i in ('left', 'right', 'up', 'down'):
            if random.random() <= 0.3:
                car= Vehicle(i, self.lightList, self.canvas, self.UNIT, self.size, self.roadLen)
                self.car_list.append(car)
    
    def car_filter(self, position):
        return [car for car in self.car_list if car.loc == position]

    def car_start_move(self, crash = None):
        if crash == None:
            self.car_list = [ car for car in self.car_list if car.step_num < car.mapSize]
            for c in self.car_list:
            # for c in [ car for car in self.car_list if car.step_num < car.mapSize]:
                if self.check_Red_Stop(c) is True or self.CarCrash(c) is True:
                    c.stop()
                else:
                    c.move()
        else:
            pass
        
    def check_Red_Stop(self, car):
        light_direction = {
            'right': 'NW',
            'left': 'SE',
            'up': 'SW',
            'down': 'NE'
        }
        light = [l for l in self.lightList if l.ID == light_direction[car.direction]]
        if len(light) != 1:
            print(f"there is something problem in check_Red")
            return
        if car.Dis_light == 0 and light[0].lightState == 'red':
            return True
        else:
            return False

    
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

    def Car(self):
        pass

    def backgound(self):
        self.title('traffic_lights')
        self.geometry(f"{self.size * self.UNIT}x{self.size * self.UNIT}")
        self.build_menu()
        self.Cross_street()
        self.light()
        self.canvas.pack()

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
        if len(new_list) == 0:
            position = 9
        else:
            position = new_list[0].Dis_light if new_list[0].Dis_light < 9 else 9

        return  position, len([car for car in new_list if car.moveState == False])
    
    # def ClosestCar(self):
    #     return self._ClosestCar(self.car_list)

    def CarCrash(self, car):
        car_list = self.car_filter(car.loc)
        car_idx = car_list.index(car)
        if car_idx == 0:
            return False
        else:
            if car_list[car_idx - 1].moveState == False:
                if  car.Dis_light - car_list[car_idx - 1].Dis_light <= 1:
                    return True
                else:
                    return False
            else:
                return False


class TrafficSimulator(traffic):
    def __init__(self):
        super(TrafficSimulator, self).__init__()
        self.action = ['stay', 'switch']
        self.n_action = len(self.action)
        self.time_stamp = 0
        self.backgound()
        self.light_NW._Change('red')
        self.light_SE._Change('red')
        self.light_NE._Change('green')
        self.light_SW._Change('green')

    def restart(self):
        self.canvas.update()
        # time.sleep(0.5)
        self.light_NW._Change('red')
        self.light_SE._Change('red')
        self.light_NE._Change('green')
        self.light_SW._Change('green')
        for i in self.car_list:
            i.can.delete(i.can_id)
        self.car_list = []
        # return [9, 9, 9, 9, "red", "green", "red", "green", 0]
        return [9, 9, "red", "green", "red", "green", 0]

    def render(self):
        self.canvas.update()
        # time.sleep(0.1)
        # self.time_stamp += 1
        # if self.time_stamp >= 1000:
        #     self.Exit()

    def step(self, action):
        """
        input:
        action swich (1) if the agent want to change the light, stay (0) otherwise.
        output:
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
        done if game is done
        info is the total number of queueing cars, which can be ploted in the report graph.
        """
        self.random_create_car()
        if action == 1:
            for i in self.lightList:
                i.Change()
            self.car_start_move()
        else:
            for i in self.lightList:
                i.ChangeDelay()
            self.car_start_move()
        
        o_list1 = self.car_filter('left')
        o_list2 = self.car_filter('up')
        o_list3 = self.car_filter('right')
        o_list4 = self.car_filter('down')

        clost1, Qnum1= self._ClosestCar(o_list1)
        clost2, Qnum2= self._ClosestCar(o_list2)
        clost3, Qnum3= self._ClosestCar(o_list3)
        clost4, Qnum4= self._ClosestCar(o_list4)

        clost_R1 = min((clost1,clost3))
        clost_R2 = min((clost2,clost4))

        info = sum([Qnum1,Qnum2,Qnum3,Qnum4])
        lightState = [ls.lightState for ls in self.lightList]
        if info == 0:
            reward = 0
        else:
            reward = -1

        # return [clost1,clost2,clost3,clost4] + lightState + [self.light_NE.Delaytime], reward, None, info
        return [clost_R1, clost_R2] + lightState + [self.light_NE.Delaytime], reward, None, info

    def test_debug(self):
        
        self.light_NW._Change('red')
        self.light_SE._Change('red')
        self.light_NE._Change('green')
        self.light_SW._Change('green')
        for t in range(10000):
            if t % 24 == 0:
                for i in self.lightList:
                    i.Change()
            self.random_create_car()
            self.car_start_move()
            time.sleep(0.2)
            self.canvas.update()

def update():
    for i in range(50):
        observation = env.restart()
        print(f"the start state {observation}")
        for j in range(1000):

            action = random.randint(0,1)
            print(f"the action is {env.action[action]}")

            observation, reward, done, info = env.step(action)
            print(observation, " ", reward," ", done," ", info)
            
            env.render()
            # time.sleep(3)

        print(f"{j} times finished.")



if __name__ == '__main__':
    env = TrafficSimulator()
    # env.test_debug()
    env.after(500, func = update)
    env.mainloop()

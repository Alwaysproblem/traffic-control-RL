import numpy as np
import time
import sys
import random
import copy

if sys.version_info.major==2:
    import Tkinter as tk
else:
    import tkinter as tk


class create_car_up(object):
    def __init__(self):
        self.x1 = 250
        self.x2 = 255
        self.y1 = 0 + 1
        self.y2 = 5 + 1

class create_car_left(object):
    def __init__(self):
        self.x1 = 0 + 1
        self.x2 = 5
        self.y1 = 250 
        self.y2 = 255 

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getPosTuple(self):
        return self.x, self.y

class Vehicle:
    def __init__(self, position, Canvas, UNIT = 10, size = 100, RoadWidth = 12):
        dire = {
            'up': 'down',
            'down': 'up',
            'left': 'right',
            'right': 'left'
        }
        self.mapSize = size
        self.pos = position                     # the car initial position
        self.direction = dire[position]         # the direction of moving
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self.road = RoadWidth
        self.can_id = None
        self.can = Canvas
        self.unit = UNIT
        func = {
            'up': self.up,
            'down': self.down,
            'left': self.left,
            'right': self.right
        }
        self.color = {
            'up': 'purple',
            'down': 'firebrick1',
            'left': 'blue4',
            'right': 'deep pink'
        }
        func[self.direction]()
    
    def up(self):
        """ calculate the postion of the car from the upper bound."""
        self.x1 = (self.mapSize//2 + self.road//4)*self.unit
        self.x2 = (self.mapSize//2 + self.road//4 + 1)*self.unit
        self.y1 = (self.mapSize)*self.unit
        self.y2 = (self.mapSize - 1)*self.unit
        self.can_id = self.can.create_rectangle(self.sp.x, self.sp.y, self.ep.x, self.ep.y, fill = 'gray')

    def down(self):
        self.x1 = (self.mapSize//2 - self.road//4 - 1)*self.unit
        self.x2 = (self.mapSize//2 - self.road//4)*self.unit
        self.y1 = 1*self.unit
        self.y2 = 0*self.unit

    def left(self):
        self.x1 = 0*self.unit
        self.x2 = 1*self.unit
        self.y1 = (self.mapSize//2 + self.road//4 + 1)*self.unit
        self.y2 = (self.mapSize//2 + self.road//4)*self.unit

    def right(self):
        self.x1 = 1*self.unit
        self.x2 = 0*self.unit
        self.y1 = (self.mapSize//2 - self.road//4)*self.unit
        self.y2 = (self.mapSize//2 - self.road//4 - 1)*self.unit
    
    def create(self):
        pass

    def cal_cord(self, direction):
        pass

    def getCarPos(self):
        return self.x1, self.x2, self.y1, self.y2

    def move(self):
        pass

    def stop(self):
        pass

class light:
    def __init__(self, source_position, length, width, Canvas, UNIT, direction = 'L'):
        """ 
        source position should be point class.
        derection should be :
        'L' left light is red 
        'R' Right light is red
        the left light is red when the road direction is up or left.
        """
        self.sp = copy.deepcopy(source_position)
        self.sp.x *= UNIT
        self.sp.y *= UNIT
        self.width = width * UNIT
        self.length = length * UNIT
        self.direction = direction
        self.mode = length >= width        # if length >= width means the light should be horizontal.
        self.changeFlag = False
        self.ep = point(self.sp.x + self.length, self.sp.y + self.width)
        self.red = None
        self.yellow = None
        self.green = None
        self.can = Canvas

    def cal_R_cod(self):
        if self.direction == 'L':
            if self.mode == True:
                return self.sp, point(self.sp.x + round(self.length / 3), self.sp.y + self.width)
            else:
                return self.sp, point(self.sp.x + self.length, self.sp.y + round(self.width / 3))
        else:
            if self.mode == True:
                return point(self.sp.x + round(self.length / 3 * 2), self.sp.y), self.ep
            else:
                return point(self.sp.x, self.sp.y + round(self.width / 3 * 2)), self.ep

    def cal_Y_cod(self):
        if self.mode == True:
            return point(self.sp.x + round(self.length / 3), self.sp.y), \
                    point(self.sp.x + round(self.length / 3 * 2), self.sp.y + self.width)
        else:
            return point(self.sp.x, self.sp.y +  + round(self.width / 3)), \
                    point(self.sp.x + self.length, self.sp.y + round(self.width / 3 * 2))

    def cal_G_cod(self):
        if self.direction == 'L':
            if self.mode == True:
                return point(self.sp.x + round(self.length / 3 * 2), self.sp.y), self.ep
            else:
                return point(self.sp.x, self.sp.y + round(self.width / 3 * 2)), self.ep
        else:
            if self.mode == True:
                return self.sp, point(self.sp.x + round(self.length / 3), self.sp.y + self.width)
            else:
                return self.sp, point(self.sp.x + self.length, self.sp.y + round(self.width / 3))

    def getFlagState(self):
        return self.changeFlag

    def draw(self):
        self.can.create_rectangle(self.sp.x, self.sp.y, self.ep.x, self.ep.y, fill = 'gray')
        point_a,point_b = self.cal_R_cod()
        self.red = self.can.create_oval(point_a.x, point_a.y, point_b.x, point_b.y, fill = 'red')
        point_a,point_b = self.cal_Y_cod()
        self.yellow = self.can.create_oval(point_a.x, point_a.y, point_b.x, point_b.y, fill = 'yellow')
        point_a,point_b = self.cal_G_cod()
        self.green = self.can.create_oval(point_a.x, point_a.y, point_b.x, point_b.y, fill = 'green')

    def _Change(self, color):
        self.changeFlag = not self.changeFlag
        dic = {
            'red': self.red,
            'yellow': self.yellow,
            'green': self.green
        }
        for i in dic.keys():
            if i == color:
                self.can.itemconfig(dic[i], fill = color)
            else:
                self.can.itemconfig(dic[i], fill = 'gray')



class traffic_lights(tk.Tk,object):
    def __init__(self):
        super(traffic_lights, self).__init__()
        self.UNIT = 10
        self.change = True
        self.car_list = []
        self.time_stamp = 0
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

        self.light_NW = light(point(self.road_point_NW.x - roadH_light_size[0], self.road_point_NW.y), *roadH_light_size, self.canvas, self.UNIT, 'L')
        self.light_SW = light(self.road_point_SW, *roadV_light_size, self.canvas, self.UNIT, 'L')
        self.light_SE = light(point(self.road_point_SE.x, self.size/2), *roadH_light_size, self.canvas, self.UNIT, 'R')
        self.light_NE = light(point(self.size/2, self.road_point_NE.y - roadV_light_size[1]), *roadV_light_size, self.canvas, self.UNIT, 'R')

        self.title('traffic_lights')
        self.geometry(f"{self.size * self.UNIT}x{self.size * self.UNIT}")
        self.build_menu()
        self.Cross_street()
        # self.light_NW.draw()
        # self.light_SW.draw()
        # self.light_SE.draw()
        # self.light_NE.draw()
        # self.light_NE._Change('green')
        self.light()
        self.canvas.pack()

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
    #     while(True):
    #         if self.car==[]:    # if there no car, then create cars in random direction
    #             if  random.random()>0.5:
    #                 self.car_1=create_car_up()
    #                 self.car1 = self.canvas.create_rectangle(self.car_1.x1,self.car_1.y1,self.car_1.x2,self.car_1.y2,fill='yellow')
    #                 self.car.append([self.car1,self.car_1])
    #             if  random.random()>0.5:
    #                 self.car_2=create_car_left()
    #                 self.car2 = self.canvas.create_rectangle(self.car_2.x1,self.car_2.y1,self.car_2.x2,self.car_2.y2,fill='blue')
    #                 self.car.append([self.car2,self.car_2])

    #         for i in self.car:              # loop, create car
    #             self.crash=0
    #             if (i[1].x1==245 and i[1].x2==255):      # the car from up
    #                 self.color_1 = self.canvas.itemcget(self.red_1, 'fill')
    #                 if (self.color_1=='red'and i[1].y1+self.speed>=215 and i[1].y1<=215): # if meat red light stop
    #                     i[1].y1+=0
    #                     i[1].y2+=0
    #                 else:
    #                     for j in self.car:
    #                         if (j!=i and j[1].x1==245 and j[1].x2==255):
    #                             if (i[1].y2+self.speed >j[1].y1 and i[1].y2<=j[1].y1):   # if it will have a crash with a other car stop
    #                                 self.crash=1
    #                                 break

    #                     if self.crash==0:   # if no crash at all, change its position
    #                         i[1].y1+=self.speed
    #                         i[1].y2+=self.speed
    #                         if(i[1].y2>=500):
    #                             self.canvas.coords(i[0],(i[1].x1,500,i[1].x2,i[1].y2))  # update car's location
    #                             self.canvas.delete(i)
    #                             self.car.remove(i)
    #                         else:
    #                             self.canvas.coords(i[0],(i[1].x1,i[1].y1,i[1].x2,i[1].y2))
    #                     else:
    #                         i[1].y1+=0
    #                         i[1].y2+=0


    #             if (i[1].y1==245  and i[1].y2==255):
    #                 self.color_2 = self.canvas.itemcget(self.red_2, 'fill')
    #                 if (self.color_2=="red"and i[1].x1+self.speed>=215 and i[1].x1<=215):
    #                     i[1].x1+=0
    #                     i[1].x2+=0
    #                     self.canvas.coords(i[0],(i[1].x1,i[1].y1,i[1].x2,i[1].y2))
    #                 else:
    #                     for j in self.car:
    #                         if (j!=i and j[1].y1==245 and j[1].y2==255):
    #                             if (i[1].x2+self.speed >j[1].x1 and i[1].x2<=j[1].x1):
    #                                 self.crash=1
    #                                 break

    #                     if self.crash==0:
    #                         i[1].x1+=self.speed
    #                         i[1].x2+=self.speed
    #                         if(i[1].x2>=500):
    #                             self.canvas.coords(i[0],(500,i[1].y1,i[1].x2,i[1].y2))
    #                             self.canvas.delete(i)
    #                             self.car.remove(i)
    #                         else:
    #                             self.canvas.coords(i[0],(i[1].x1,i[1].y1,i[1].x2,i[1].y2))
    #                     else:
    #                         i[1].x1+=0
    #                         i[1].x2+=0

    #         if (self.time_stamp % 3==0): # when it loop 3 times ,the cars start to be created
    #             if  random.random()>0.5:   # randomly create cars, 50%
    #                 self.car_1=create_car_up()
    #                 self.car1 = self.canvas.create_rectangle(self.car_1.x1,self.car_1.y1,self.car_1.x2,self.car_1.y2,fill='yellow')
    #                 self.car.append([self.car1,self.car_1])

    #         if(self.time_stamp % 2==0):
    #             if random.random()>0.5:
    #                 self.car_2=create_car_left()
    #                 self.car2 = self.canvas.create_rectangle(self.car_2.x1,self.car_2.y1,self.car_2.x2,self.car_2.y2,fill='blue')
    #                 self.car.append([self.car2,self.car_2])

    #         self.time_stamp += 1
    #         if (self.time_stamp % 3 == 0):
    #             self.light_change()
    #         self.update()
    #         time.sleep(0.25)  #system sleep 0.25
            
    def backgound(self):
        pass

if __name__ == '__main__':
    env = traffic_lights()
    # env.Cross_street()
    env.mainloop()

from Point import point

class Vehicle:
    def __init__(self, location, all_light, Canvas = None, UNIT = 10, size = 100, RoadWidth = 12):
        dire = {
            'up': 'down',
            'down': 'up',
            'left': 'right',
            'right': 'left'
        }
        self.mapSize = size
        self.loc = location                     # the car initial location
        self.direction = dire[self.loc]         # the direction of moving
        self.sp = point(0, 0)                   # start point 
        self.ep = point(0, 0)                       # end point
        self.can_id = None
        self.road = RoadWidth
        self.can = Canvas
        self.unit = UNIT
        self.speed = self.unit
        intial_fun = {
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
        self.step_num = 1  # if step number > 100 delete the car from canvas.
        self.moveState = True
        self.all_light = all_light
        self.Dis_light = None
        # intial function:
        intial_fun[self.loc]()
        self.create()
        self.cal_distance_from_light()
    
    def up(self):
        """ calculate the postion of the car from the upper bound."""
        x1 = (self.mapSize//2 + self.road//4) * self.unit
        x2 = (self.mapSize//2 + self.road//4 + 1) * self.unit
        y1 = 0 * self.unit
        y2 = 1 * self.unit

        self.sp = point(x1, y1)
        self.ep = point(x2, y2)

    def down(self):
        x1 = (self.mapSize//2 - self.road//4 - 1) * self.unit
        y1 = (self.mapSize - 1) * self.unit
        x2 = (self.mapSize//2 - self.road//4) * self.unit
        y2 = (self.mapSize) * self.unit

        self.sp = point(x1, y1)
        self.ep = point(x2, y2)

    def left(self):
        x1 = 0 * self.unit
        x2 = 1 * self.unit
        y1 = (self.mapSize//2 - self.road//4 - 1) * self.unit
        y2 = (self.mapSize//2 - self.road//4) * self.unit

        self.sp = point(x1, y1)
        self.ep = point(x2, y2)

    def right(self):
        x1 = (self.mapSize - 1) * self.unit
        x2 = (self.mapSize) * self.unit
        y1 = (self.mapSize//2 + self.road//4) * self.unit
        y2 = (self.mapSize//2 + self.road//4 + 1) * self.unit

        self.sp = point(x1, y1)
        self.ep = point(x2, y2)
    
    def create(self):
        if self.can != None:
            self.can_id = self.can.create_rectangle(self.sp.x, self.sp.y, self.ep.x, self.ep.y, fill = self.color[self.loc])
            

    def getStep(self):
        return self.step_num

    def distroy(self):
        if self.step_num >= self.mapSize:
            self.can.delete(self.can_id)

    def cal_distance_from_light(self):
        light_dic = {
            'left': 'SE',
            'right': 'NW',
            'up': 'SW',
            'down': 'NE'
        }
        filt_light = [light for light in self.all_light if light.ID == light_dic[self.direction]]
        if len(filt_light) != 1:
            print(f'there will be something not right\nhere is the {filt_light}')
            return

        if self.direction == 'left':
            self.Dis_light = (self.sp.x - filt_light[0].ep.x) / self.unit
        elif self.direction == 'down':
            self.Dis_light = (filt_light[0].sp.y - self.ep.y) / self.unit
        elif self.direction == 'right':
            self.Dis_light = (filt_light[0].sp.x - self.ep.x) / self.unit
        elif self.direction == 'up':
            self.Dis_light = (self.sp.y - filt_light[0].ep.y) / self.unit
        else:
            pass

    def cal_cord_after_move(self):
        if self.direction == 'right':
            self.sp.x += self.speed                          #left
            self.ep.x += self.speed
        elif self.direction == 'down':
            self.sp.y += self.speed                          #down
            self.ep.y += self.speed
        elif self.direction == 'left':
            self.sp.x -= self.speed                          #right
            self.ep.x -= self.speed
        elif self.direction == 'up':
            self.sp.y -= self.speed                          #up
            self.ep.y -= self.speed
        else:
            pass

    def getCarPos(self):
        return self.sp, self.ep

    def move(self):
        self.moveState = True
        if self.direction == 'left':
            self.can.move(self.can_id, -self.speed, 0)      #left
        elif self.direction == 'down':
            self.can.move(self.can_id, 0, self.speed)      #down
        elif self.direction == 'right':
            self.can.move(self.can_id, self.speed, 0)     #right
        elif self.direction == 'up':
            self.can.move(self.can_id, 0, -self.speed)     #up
        else:
            pass

        # self.can.tag_raise(self.can_id)
        self.cal_cord_after_move()
        self.cal_distance_from_light()
        self.step_num += 1
        self.distroy()

    def stop(self):
        self.moveState = False

    def show(self):
        print(f"this car location is ({self.sp.x}, {self.sp.y}) and ({self.ep.x}, {self.ep.y})")
        print(f"the distance from light is {self.Dis_light} UNIT.")


if __name__ == '__main__':
    pass
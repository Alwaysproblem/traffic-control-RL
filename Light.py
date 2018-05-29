from Point import point
import copy

class light:
    def __init__(self, source_position, length, width, Canvas, UNIT, ID, direction = 'L'):
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
        self.ID = ID


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
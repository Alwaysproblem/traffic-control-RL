class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # def __lt__(self, other):
    #     return self.x < other.x

    # def __eq__(self, other):
    #     return  self.x == other.x

    # def __ne__(self, other):
    #     return self.x != other.x
    
    # def __ge__(self, other):
    #     return self.x >= other.x

    # def __gt__(self, other):
    #     return self.x > other.x

    def getPosTuple(self):
        return self.x, self.y

    def show(self):
        print(f"({self.x}, {self.y})")
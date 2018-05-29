class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getPosTuple(self):
        return self.x, self.y

    def show(self):
        print(f"({self.x}, {self.y})")
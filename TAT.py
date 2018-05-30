from Car import Vehicle
import tkinter as tk
from queue import PriorityQueue as PQ
import random as rd
from Point import point
from traffic_sim import traffic
# C = tk.Canvas(bg = "white", height = 100, width = 100)

# a = Vehicle('left', C)
# b = Vehicle('right', C)

# class myPQ(PQ):
#     def _get_priority(self, item):
#         return item.x
    
#     def _get(self):
#         super()._get()[1]

#     def _put(self, item):
#         super()._put((self._get_priority(item), item))

# p = myPQ(100)

# list_p = [point(rd.randint(1,10), rd.randint(1,10)) for _ in range(10)]

# for i in list_p:
#     i.show()

# print()

# def sort_key(x):
#     return x.y

# list_p.sort(key = sort_key)

# for i in list_p:
#     i.show()

# for i in list_p:
#     p.put(i)

# for _ in range(5):
#     print(p.get())

env = traffic()


list_car = [Vehicle('left', env.lightList, env.canvas, env.UNIT, env.size, env.roadLen) for _ in range(10)]

for i in list_car:
    i.Dis_light = rd.randint(-10, 10)
    print(i.Dis_light)


print()
print(env.closestcar(list_car))


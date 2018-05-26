from traffic_sim import Vehicle
import tkinter as tk

C = tk.Canvas(bg = "white", height = 100, width = 100)

a = Vehicle('left', C)

print(a.x1)
print(a.can_id)
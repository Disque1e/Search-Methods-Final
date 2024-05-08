import math
import tkinter as tk
from PIL import Image, ImageTk
import Database as DB
import time


class MapWindow:
    def __init__(self, master, Wpath, path, wholePath, start, dest):
        self.master = master
        self.master.title("Map")
        self.master.geometry("500x900")
        self.Wpath = Wpath
        self.path = path
        self.wholePatch = wholePath
        self.start = start
        self.dest = dest
        self.steps = 50
        self.delay = 0.05
        SQUARE_SIZE = 20

        GRID_X = 100
        GRID_Y = 50

        CANVAS_WIDTH = 500
        CANVAS_HEIGHT = 800

        canvas = tk.Canvas(self.master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        canvas.configure(scrollregion=(0, -10, 15, 23))
        canvas.pack()

        map_image = Image.open("map.png")
        map_image = map_image.resize((int(map_image.width * 1.3), int(map_image.height * 1.3)))
        self.map_photo = ImageTk.PhotoImage(map_image)
        self.map = canvas.create_image(CANVAS_WIDTH / 2 - 10, CANVAS_HEIGHT / 2 - 40, image=self.map_photo)

        car_image = Image.open("car.png")
        car_image = car_image.resize((car_image.width // 20, car_image.height // 20))
        self.car_photo = ImageTk.PhotoImage(car_image)

        start_pos = DB.positions[self.start]
        self.car = canvas.create_image(GRID_X + start_pos[0] * SQUARE_SIZE, GRID_Y + start_pos[1] * SQUARE_SIZE,
                                       image=self.car_photo)

        def draw_line(p1, p2):
            x1, y1 = p1
            x2, y2 = p2
            canvas.create_line(GRID_X + x1 * SQUARE_SIZE, GRID_Y + y1 * SQUARE_SIZE,
                               GRID_X + x2 * SQUARE_SIZE, GRID_Y + y2 * SQUARE_SIZE)

        def draw_circle(p, name):
            x, y = p

            def create_oval_color(color):
                canvas.create_oval(GRID_X + x * SQUARE_SIZE - 5, GRID_Y + y * SQUARE_SIZE - 5,
                                   GRID_X + x * SQUARE_SIZE + 5, GRID_Y + y * SQUARE_SIZE + 5, fill=color)

            if name == self.start:
                create_oval_color('green')
            elif name == self.dest:
                create_oval_color('red')
            else:
                create_oval_color('black')
            canvas.create_text(GRID_X + x * SQUARE_SIZE + 10, GRID_Y + y * SQUARE_SIZE, text=name, anchor='w')

        for p1 in DB.positions:
            for p2 in DB.connections[p1]:
                draw_line(DB.positions[p1], DB.positions[p2])
            draw_circle(DB.positions[p1], p1)

        def show_path():
            city_positions = [DB.positions[city] for city in self.path]
            end_pos = []
            for i in range(len(city_positions) - 1):
                start_pos = city_positions[i]
                end_pos = city_positions[i + 1]
                distance = math.dist(start_pos, end_pos) * SQUARE_SIZE
                x_step = (end_pos[0] - start_pos[0]) / self.steps
                y_step = (end_pos[1] - start_pos[1]) / self.steps
                for j in range(self.steps):
                    x = start_pos[0] + j * x_step
                    y = start_pos[1] + j * y_step
                    canvas.coords(self.car, GRID_X + x * SQUARE_SIZE, GRID_Y + y * SQUARE_SIZE)
                    canvas.update()
                    time.sleep(self.delay)
            # update the car's position to the final destination
            canvas.coords(self.car, GRID_X + end_pos[0] * SQUARE_SIZE, GRID_Y + end_pos[1] * SQUARE_SIZE)
            canvas.update()

        btn1 = tk.Button(self.master, text="Show Path", command=show_path)
        btn2 = tk.Button(self.master, text="Close", command=self.go_back)

        btn1.place(relx=0.4, rely=0.9, anchor=tk.CENTER)
        btn2.place(relx=0.6, rely=0.9, anchor=tk.CENTER)

    def go_back(self):
        self.master.destroy()
        self.Wpath.deiconify()

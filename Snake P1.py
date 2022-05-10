from random import randint
from time import sleep
from tkinter import Canvas, Tk

W = 20
H = 20
D = 20

DIR = {
    'Up': (0, -1),
    'Down': (0, 1), 
    'Left': (-1, 0),
    'Right': (1, 0) }

class Snake:
    def check(self, food):
        return self.canvas.coords(self.object) == self.canvas.coords(food.object)

    def __init__(self, canvas: Canvas) -> None:
        self.canvas = canvas
        self.object = canvas.create_rectangle(0, 0, D, D, fill='black')
        canvas.move(self.object, W // 2 * D, H // 2 * D)
        self.dir = (1, 0)

    def move(self):
        dx, dy = self.dir
        canvas.move(self.object, dx * D, dy * D)
    
    def rule(self, event):
        key = event.keysym
        self.dir = DIR[key]
    


class Food:
    def __init__(self, canvas: Canvas) -> None:
        self.canvas = canvas
        self.object = canvas.create_rectangle(0, 0, D, D, fill='red')
        self.place()
    
    def place(self):
        x, y = randint(0, W - 1) * D,  randint(0, H - 1) * D
        self.canvas.coords(self.object, x, y, x + D, y + D)

tk = Tk()
canvas = Canvas(tk, width = W * D, height = H * D, bg='white')
canvas.pack()
snake = Snake(canvas)
food = Food(canvas)
canvas.bind_all("<Key>", snake.rule)

while True:
    snake.move()
    if snake.check(food):
        food.place()
    canvas.update()
    sleep(0.2)


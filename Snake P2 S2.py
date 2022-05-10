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
    def __init__(self, canvas = Canvas) -> None:
        self.canvas = canvas
        self.head = Cell(canvas, W // 2, H // 2)
        self.head.dir = (1, 0)
    
    def move(self):
        self.head.move()

    def check(self, food):
        return self.head.get_coords() == food.get_coords()
    
    def rule(self, event):
        key = event.keysym
        self.head.dir = DIR[key]
    

    
class Cell:
    def __init__(self, canvas: Canvas, x = 0, y = 0, color = 'black') -> None:
        self.canvas = canvas
        self.object = canvas.create_rectangle(0, 0, D, D, fill=color)
        canvas.move(self.object, x * D, y * D)        

    def move(self):
        dx, dy = self.dir
        x, y = self.get_coords()
        self.set_coords((x + dx) % W, (y + dy) % H)   

    def get_coords(self):
        x, y, xx, yy = self.canvas.coords(self.object)
        return x // W, y // W

    def set_coords(self, x, y):
        self.canvas.coords(self.object, x * W, y * H, x * W + D, y * H + D)

class Food (Cell):
    def __init__(self, canvas: Canvas, x=0, y=0, color='black') -> None:
        super().__init__(canvas, x, y, 'red')
        self.place()
    
    def place(self):
        x, y = randint(0, W - 1),  randint(0, H - 1)
        self.set_coords(x, y)

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


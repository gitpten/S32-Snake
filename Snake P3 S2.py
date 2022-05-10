from random import randint
from time import sleep
from tkinter import Canvas, Tk, mainloop

W = 20
H = 20
D = 20

DIR = {
    'Up': (0, -1),
    'Down': (0, 1), 
    'Left': (-1, 0),
    'Right': (1, 0) }

class Snake:
    def __init__(self, canvas: Canvas, n = 3) -> None:
        self.canvas = canvas
        self.head = Cell(canvas, W // 2, H // 2)
        self.head.dir = (1, 0)
        self.tail = [self.head]
        for i in range(n - 1):
            self.add()
            self.move()
    
    def move(self):
        self.head.move()
        for i in range(len(self.tail) - 1, 0, -1):
            self.tail[i].move()
            self.tail[i].dir = self.tail[i - 1].dir
    
    def add(self):
        cell = Cell(self.canvas)
        x, y = self.tail[-1].get_coords()
        cell.set_coords(x, y)
        cell.dir = (0, 0)
        self.tail.append(cell)
    
    def check(self, food):
        return self.head.get_coords() == food.get_coords()
    
    def rule(self, event):
        key = event.keysym

        if DIR[key] == opposite(self.head.dir):            
            self.reverse()            
        else:
            self.head.dir = DIR[key]
    
    def reverse(self):
        self.head = self.tail[-1]
        self.tail.reverse()
        for i in range(len(self.tail) - 1, 0, -1):
            self.tail[i].dir = opposite(self.tail[i - 1].dir)
        self.head.dir = opposite(self.head.dir)

    def collapse(self):
        for cell in self.tail:
            if cell == self.head:
                continue
            if self.check(cell):
                cell.canvas.itemconfig(cell.object, fill='yellow')
                return True
        return False

class Cell:
    def __init__(self, canvas: Canvas, x = 0, y = 0, color = 'black') -> None:
        self.canvas = canvas
        self.object = canvas.create_rectangle(0, 0, D, D, fill=color)
        canvas.move(self.object, x * D, y * D)
        self.dir = (0, 0)

    def move(self):
        x, y = self.get_coords()
        dx, dy = self.dir
        self.set_coords((x + dx) % W, (y + dy) % H)
    
    def get_coords(self):
        x, y, x1, y1 = self.canvas.coords(self.object)
        return x // W, y // H

    def set_coords(self, x, y):
        self.canvas.coords(self.object, x * W, y * H, x * W + D, y * H + D)

class Food(Cell):
    def __init__(self, canvas: Canvas, x=0, y=0, color='black') -> None:
        super().__init__(canvas, x, y, 'red')        
        self.place()
    
    def place(self):
        x, y = randint(0, W - 1),  randint(0, H - 1)
        self.set_coords(x, y)

def opposite(dir):
    dx, dy = dir
    return (dx * -1, dy * -1)

tk = Tk()
canvas = Canvas(tk, width = W * D, height = H * D, bg='white')
canvas.pack()
snake = Snake(canvas)
food = Food(canvas)
canvas.bind_all("<Key>", snake.rule)


while not snake.collapse():
    snake.move()
    if snake.check(food):
        food.place()
        snake.add()
    canvas.update()
    sleep(0.2)

mainloop()
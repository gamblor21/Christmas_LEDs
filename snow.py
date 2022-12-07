import time
from random import randint, uniform

class Snow():
    def __init__(self, pixels, column, speed = 0.3, color=(200,240,255), height=20):
        self.pixels = pixels
        self.column = column
        self.speed = speed
        self.color = color
        self.height = height

        self.row = -1
        self.lastshown = False
        self.nextmove = time.monotonic() + uniform(0,6)

    def update(self):
        t = time.monotonic()
        if t > self.nextmove:
            self.nextmove = t + self.speed

            if self.lastshown is True:
                self.pixels[self.column*self.height + self.row] = 0
                self.lastshown = False
            self.row += 1
            if self.row >= self.height:
                self.row = -1
                self.nextmove += randint(1,5)

            color = self.pixels[self.column*self.height+self.row]

            if color[0] == 0 and color[1] == 0 and color[2] == 0:
                self.pixels[self.column*self.height+self.row] = self.color
                self.lastshown = True

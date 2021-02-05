from p5 import *
from math import pi, sin, cos, asin

cells = []
layout = "spiral" # grid / spiral
max_factors = 0

class Cell:
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n
        self.factors = []
    
    def link_factors(self):
        push_style()
        stroke(360-(len(self.factors)/max_factors)*360, 0.9, 0.9, 0.5)
        for c in self.factors:
            line((self.x, self.y), (c.x, c.y))
        pop_style()
    
    def draw_me(self):
        push_style()
        no_stroke()
        if len(self.factors) > 0:
            fill(0, 0, 1)
        else:
            stroke(198, 1, 1)
            stroke_weight(2)
            fill(120, 1, 1)
        circle(self.x, self.y, 20 if len(self.factors) else 25)
        fill(0, 0, 0)
        no_stroke()
        text_align("CENTER", "CENTER")
        text(str(self.n), self.x, self.y)
        pop_style()

def setup():
    global max_factors
    size(1200, 1200)
    color_mode('HSB', 360, 1, 1, 1)
    max_factors = 0
    
    if layout == "grid":
        cnum = 20
        cellsize = width/cnum
        i = 1
        for y in range(cnum):
            for x in range(cnum):
                c = Cell(x*cellsize+cellsize/2, y*cellsize+cellsize/2, i)
                cells.append(c)
                i += 1
    elif layout == "spiral":
        r_delta = 1 # how much to expand the radius each step
        dist = 20
        cr = 20 # radius of the circle we're drawing later
        a = 0
        i = 2
        cells.append(Cell(width/2, height/2, 1)) # center first
        cells[0].factors = [cells[0]] # 1 is not prime. dodge by putting a ref to itself in factors list
        while dist < (width/2+cr/2):
            x = cos(a) * dist + width/2
            y = sin(a) * dist + height/2
            c = Cell(x, y, i)
            cells.append(c)
            i += 1
            dist += (i**3)**-0.15 + (1.8 if i < 20 else 0.8) #r_delta
            # determine what angle to draw the next circle at given the current radius
            da = asin(cr / dist)
            a = (a + da) % (pi*2)
    
    # sort out factors
    for i, c in enumerate(cells[1:-1]):
        f = c.n # cell value
        for cf in cells[i+2:]:
            if cf.n % f == 0:
                cf.factors.append(c) # put a ref to this cell onto it factors list
                if len(cf.factors) > max_factors:
                    max_factors = len(cf.factors)
    no_loop()

def draw():
    background(0, 0, 0)
    for c in cells:
        c.link_factors()
    for c in cells:
        c.draw_me()
    save_frame("d13.png")
run()

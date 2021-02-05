# one grows, one prunes
# have a process attach to a random node and start eating
# once enough nodes have been eaten, another process attaches to a random node
# and starts repairing links (don't destroy actual nodes, just toggle states)
from p5 import *
from random import random, choice, randint, shuffle
from math import sin, cos, pi

cellsize = 200
ttl = 10
maxval = 100 # max cell value for growing purposes, hue value

class Cell:
    def __init__(self, coordinates):
        self.coords = coordinates
        # neighbour refs
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.col = (1, 0.7, 0.7)
        self.val = 1 # don't go below 1
        
        # flower stuff
        self.center = random() * 5 + 5
        self.mid_colour = (0, 0, 1)
        self.petal_colour = choice(((51, 0.78, 0.95), (61, 0.85, 0.98), (283, 0.39, 0.86), (313, 0.39, 0.93)))
        self.num_petals = randint(8, 12)
        self.petal_deltas = []
        for p in range(self.num_petals):
            pr = randint(30, 50)
            d1 = random()*pr*0.5 + pr*0.3
            d2 = random()*pr*0.5 + pr*0.3
            self.petal_deltas += [(pr, d1, d2)]
    
    def draw_me(self):
        stroke(0)
        stroke_weight(1)
        
        # draw a flower according to the cell's value
        if self.val < (maxval / 10): # 10% of max value doesn't get a flower
            return
        
        petals = []
        p_a = pi*2/self.num_petals
        scale = self.val / maxval
        sx, sy = self.coords[0]*cellsize+cellsize/2, self.coords[1]*cellsize+cellsize/2
        for i, pd in zip(range(self.num_petals), self.petal_deltas):
            p = [(sx, sy), (sx, sy)]
            p += [(cos(i*p_a-p_a/2)*pd[1]*scale+sx, sin(i*p_a-p_a/2)*pd[2]*scale+sy)]
            p += [(cos(i*p_a)*pd[0]*scale+sx, sin(i*p_a)*pd[0]*scale+sy)] # mid point
            p += [(cos(i*p_a+p_a/2)*pd[1]*scale+sx, sin(i*p_a+p_a/2)*pd[2]*scale+sy)]
            p += [(sx, sy), (sx, sy)]
            petals.append(p)
        
        fill(*self.petal_colour)
        for petal in petals:
            begin_shape()
            for p in petal:
                curve_vertex(*p)
            end_shape()
        fill(*self.mid_colour)
        circle(sx, sy, self.center*scale)
    
    def get_coords(self):
        return self.coords
    
    def show(self, eater):
        stroke_weight(4)
        no_fill()
        if eater:
            stroke(0, 1, 1)
        else:
            stroke(114, .75, .75)
        circle(self.coords[0]*cellsize+cellsize/2, self.coords[1]*cellsize+cellsize/2, cellsize/2)
    
    def __repr__(self):
        return f"({self.coords}) {'<' if self.left else ''}{'>' if self.right else ''}{'v' if self.down else ''}{'^' if self.up else ''}"

class Grid:
    def __init__(self, w, h):
        self.h = h
        self.w = w
        self.cells = {}
        for y in range(h):
            for x in range(w):
                self.cells[x, y] = Cell((x, y))
    
    def get_cell_at(self, coordinates):
        return self.cells[coordinates]
    
    def draw_me(self):
        for cell in self.cells:
            self.cells[cell].draw_me()

class Agent:
    def __init__(self, grid, start=None, eater=False):
        self.grid = grid
        if not start:
            self.coords = int(random()*grid.w), int(random()*grid.h)
        else:
            self.coords = start
        self.eater = eater
        self.ttm = ttl # time to move in frames, maybe make eaters move faster as they eat more and slower with less food?
        self.time_left = self.ttm
        self.strength = random()*5 * 1 if not eater else -1
    
    def calc_weights(self):
        # Caluclate the values of surrounding cells as a movement target, return them as a percentage
        # of total value of connnected cells
        here = self.grid.get_cell_at(self.coords)
        t = sum((x.val for x in (here.left, here.right, here.up, here.down) if x))
        n = {x: (x.val/t) for x in (here.left, here.right, here.up, here.down) if x}
        return n
    
    def move(self):
        self.time_left -= 1
        if self.time_left > 0:
            return
        else:
            self.time_left = self.ttm
        
        nxt = self.calc_weights()
        
        # use the random value to pick a neighbour to move to
        # eaters prefer high values, growers prefer low values
        r = random()
        k = list(nxt)
        shuffle(k)
        for c in k:
            v = (1 - nxt[c]) if not self.eater else nxt[c]
            r -= v
            if r < 0:
                self.coords = c.get_coords()
                break
        
    
    def modify(self):
        self.grid.cells[self.coords].val += self.strength
        if self.grid.cells[self.coords].val < 1:
            self.grid.cells[self.coords].val = 1
        elif self.grid.cells[self.coords].val > maxval:
            self.grid.cells[self.coords].val = maxval
    
    def show(self):
        self.grid.get_cell_at(self.coords).show(self.eater)

def setup():
    global grid, eater, grower
    size(800, 800)
    color_mode('HSB', 360, 1, 1, 1)
    
    #no_loop()
    
    grid = Grid(int(width/cellsize), int(height/cellsize))
    eater = Agent(grid, eater=True)
    grower = Agent(grid)
    
    # link cells in grid
    for y in range(int(height/cellsize)):
        for x in range(int(width/cellsize)):
            if x > 0:
                grid.cells[x, y].left = grid.cells[x-1, y]
            if x < int(width/cellsize)-2:
                grid.cells[x, y].right = grid.cells[x+1, y]
            if y > 0:
                grid.cells[x, y].up = grid.cells[x, y-1]
            if y < int(height/cellsize)-2:
                grid.cells[x, y].down = grid.cells[x, y+1]

def draw():
    background(128, 0.62, .54)
    
    # modify the values of the grid location according to eater/grower rules
    eater.modify()
    grower.modify()
    
    eater.move()
    grower.move()
    
    grid.draw_me()
    
    eater.show()
    grower.show()
    
    save_frame("d:/tmp/frames/petal.png")
    
    if frame_count > 1500:
        no_loop()
        print("Done.")

run()
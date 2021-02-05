# Genuary Day 2
# triangular cellular automata, one row per generation
# orientation of the triangles is dependent on the previous row

from random import randint

COLOUR = True
ROTATE = True
CUR_SHAPE = "circle" # circle, triangle, curve

d = 810
cellsize = 20
cells = {}

colour_range = random(50,310)

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.val = 0
        self.rotation = 0
        if COLOUR:
            self.colour = [random(colour_range-50,colour_range+50),0.5,0]
        else:
            self.colour = [0, 0, 0]
    
    def get_states(self, state = 0):
        states = {
                  "111": [0, 50, 0.1, 0],
                  "110": [0, 30, 0.05, QUARTER_PI/4],
                  "101": [0, 30, 0.05, 0],
                  "100": [1, 10, -0.05, QUARTER_PI/2],
                  "011": [1, 30, -0.05, -QUARTER_PI/4],
                  "010": [1, 5, -0.05, 0],
                  "001": [1, 5, -0.05, -QUARTER_PI/2],
                  "000": [0, 0, 0, 0],
                  }
        try:
            left = str(cells[self.y-1][self.x-1].val)
        except KeyError:
            left = "1" if random(1) > 0.5 else "0"
        try:
            right = str(cells[self.y-1][self.x+1].val)
        except KeyError:
            right = "1" if random(1) > 0.5 else "0"
        top = str(cells[self.y-1][self.x].val)
        
        return states[left+top+right][state]
    
    def choose_shape(self):
        # get a fill value
        self.val = self.get_states()
        # get colour mods
        if COLOUR:
            self.colour[0] += self.get_states(state=1)
            self.colour[1] += self.get_states(state=2)
            
            # check bounds
            if self.colour[0] > 360:
                self.colour[0] = 360
            elif self.colour[0] < 0:
                self.colour[0] = 0
            if self.colour[1] > 1.0:
                self.colour[1] = 1.0
            elif self.colour[1] < 0.5:
                self.colour[1] = 0.5
        else:
            self.colour[1] = 0
            self.colour[2] = self.val
        
        if ROTATE:
            self.rotation = self.get_states(state=3)
    
    def draw_me(self):
        pushStyle()
        noStroke()
        c = self.colour[:]
        if COLOUR:
            c[2] = 0 if self.val else 1
            c[1] = 0.5 if self.val else 0.5#c[1]
        if c[2] == 0:
            return
        fill(*c)
        
        # choose a random fill shape
        if CUR_SHAPE == "circle":
            sz = random(cellsize*0.3,cellsize*1.3)
            circle(self.x * cellsize + cellsize/2.0, self.y * cellsize + cellsize/2.0, sz)
            blendMode(MULTIPLY)
            c[2] *= 0.6
            c[1] *= 0.8
            c[0] += random(-20,20)
            cx, cy = self.x * cellsize + cellsize/2.0 + random(-5,5), self.y * cellsize + cellsize/2.0 + random(-5,5)
            circle(cx, cy, sz*0.7)
            colorMode(DIFFERENCE)
            cx += random(-3,3)
            cy += random(-3,3)
            c[2] *= 1.1
            c[1] *= 0.3
            c[0] += random(-50,50)
            circle(self.x * cellsize + cellsize/2.0 + random(-5,5), self.y * cellsize + cellsize/2.0 + random(-5,5), sz*0.4)
        elif CUR_SHAPE == "triangle":
            a = radians(30) + self.rotation
            sz = random(cellsize*0.3, cellsize*0.6)
            beginShape()
            for i in range(3):
                x, y = cos(i*TWO_PI/3.0+a) * sz + self.x * cellsize + cellsize*0.5, sin(i*TWO_PI/3+a) * sz + self.y * cellsize + cellsize*0.5
                vertex(x, y)
            endShape(CLOSE)
        elif CUR_SHAPE == "curve":
            stroke(0,0,1)
            strokeWeight(1)
            noFill()
            beginShape()# mid to bottom right
            curveVertex(self.x * cellsize + cellsize/2.0, self.y * cellsize)
            curveVertex(self.x * cellsize + cellsize/2.0, self.y * cellsize)
            curveVertex(self.x * cellsize + cellsize/2.0, self.y * cellsize + cellsize/2.0)
            curveVertex(self.x * cellsize + cellsize, self.y * cellsize + cellsize)
            curveVertex(self.x * cellsize + cellsize, self.y * cellsize + cellsize)
            endShape()
            beginShape()# mid to bottom left
            curveVertex(self.x * cellsize + cellsize/2.0, self.y * cellsize)
            curveVertex(self.x * cellsize + cellsize/2.0, self.y * cellsize)
            curveVertex(self.x * cellsize + cellsize/2.0, self.y * cellsize + cellsize/2.0)
            curveVertex(self.x * cellsize, self.y * cellsize + cellsize)
            curveVertex(self.x * cellsize, self.y * cellsize + cellsize)
            endShape()
            # beginShape() # mid to mid
            # curveVertex(self.x * cellsize + cellsize/2.0, self.y * cellsize)
            # curveVertex(self.x * cellsize + cellsize/2.0, self.y * cellsize)
            # curveVertex(self.x * cellsize + cellsize/2.0, self.y * cellsize + cellsize/2.0)
            # curveVertex(self.x * cellsize + cellsize/2, self.y * cellsize + cellsize)
            # curveVertex(self.x * cellsize + cellsize/2, self.y * cellsize + cellsize)
            # endShape()
            
            
        popStyle()

for y in range(d/cellsize):
    cells[y] = {}
    for x in range(d/cellsize):
        cells[y][x] = Cell(x,y)
        if y == 0:
            cells[y][x].val = randint(0,1)
            cells[y][x].colour[2] = cells[y][x].val

def setup():
    size(d, d)
    colorMode(HSB, 360, 1, 1, 1)
    background(0)
    noLoop()
    

def draw():
    for y in range(1,len(cells)):
        # process each row
        for x in cells[y]:
            cells[y][x].choose_shape()
    
    for y in cells:
        for x in cells[y]:
            cells[y][x].draw_me()
    
    saveFrame("Day2.png")

cellsize = 200
cells = {}

recording = False

class Cell:
    def __init__(self, x, y, ix, iy):
        self.x, self.y = x, y
        self.ix, self.iy = ix, iy # positional indices
        self.xdiv = 1.0
        self.ydiv = 1.0
        self.left = None
        self.up = None
    
    def left_inter(self):
        if self.left:
            return self.f(frameCount)[0] + self.left.left_inter()
        else:
            return self.f(frameCount)[0]
    
    def up_inter(self):
        if self.up:
            return self.f(frameCount)[1] + self.up.up_inter()
        else:
            return self.f(frameCount)[1]
    
    def f(self, fc):
        return cos(fc/self.xdiv), sin(fc/self.ydiv)
    
    def draw_me(self):
        pushStyle()
        pushMatrix()
        translate(self.x, self.y)
        fill(0, 0, 1)
        noStroke()
        circle(0, 0, 5)
        
        # calculate interference from previous cells
        # average out based on position
        ix = self.left_inter() / self.ix
        iy = self.up_inter() / self.iy

        fill(0, 1, 1, 0.5)
        circle(ix*cellsize*0.3, iy*cellsize*0.3, 2)
        
        popMatrix()
        popStyle()
    
    def __repr__(self):
        return "{}, {}".format(self.x, self.y)

def setup():
    size(800, 800)
    colorMode(HSB, 360, 1, 1, 1)
    background(0, 0, 0)
    
    for x in range(4):
        for y in range(4):
            cells[x,y] = Cell(x*cellsize+cellsize/2, y*cellsize+cellsize/2, x+1, y+1)
            cells[x,y].xdiv, cells[x,y].ydiv = 100.0, 100.0
    # set up neighbour properties
    for y in range(4):
        for x in range(4):
            if x != 0:
                cells[x,y].left = cells[x-1,y]
            if y != 0:
                cells[x,y].up = cells[x,y-1]
    
    cells[0,0].xdiv, cells[0,0].ydiv = 100.0, 100.0
    
    # set up vertical seeds
    for i in range(1,4):
        cells[0,i].xdiv, cells[0,i].ydiv = random(50, 100), random(30, 50)
    
    # set up horizontal seeds
    for i in range(1,4):
        cells[i,0].xdiv, cells[i,0].ydiv = random(30, 50), random(50, 100)

def draw():
    noStroke()
    fill(0, 0, 0, 0.04)
    square(0, 0, height)
    for k in cells:
        cells[k].draw_me()
    
    if recording and frameCount < 1500:
        saveFrame("frames/#####.png")
    else:
        noLoop()
        print("Done.")

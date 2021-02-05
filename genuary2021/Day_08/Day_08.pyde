spiral_down = []
spiral_up = []

s_radius = 100
s_space = 10
ymove_speed = 1
xmove_speed = 1

minx, maxx, miny, maxy = 0, 0, 0, 0

class Spiral:
    def __init__(self, x, y, r, num, spacing, a, offset = 0):
        self.x = x
        self.y = y
        self.r = r
        self.num = num
        self.spacing = spacing
        self.a = a
        self.offset = offset
        self._stroke = (0, 0, 0.7)
        self.off = 0
    
    def draw_me(self):
        pushStyle()
        noFill()
        #stroke(*self._stroke)
        strokeWeight(1)
        hsteps = 360.0 / self.num
        
        r = self.r
        for i in range(self.num):
            if self.off:
                stroke(i*hsteps, 0.3, 0.7)
            else:
                stroke((self.num-i)*hsteps, 0.3, 0.7)
            arc(self.x, self.y, r, r, self.offset, self.offset + self.a)
            r -= self.spacing
        popStyle()
    
    def move(self, yoff, xoff=0):
        self.y += yoff
        self.x += xoff
        if self.y > maxy:
            self.y =  miny
        elif self.y < miny:
            self.y = maxy
            
        if self.x > maxx:
            self.x = minx
        elif self.x < minx:
            self.x = maxx

def setup():
    global spiral_down, spiral_up, minx, maxx, miny, maxy
    size(800, 800)
    colorMode(HSB, 360, 1, 1, 1)
    #blendMode(MULTIPLY)
    
    
    rows = height / (s_radius/2) + 4
    cols = width / (s_radius/2) + 4
    
    miny = -s_radius * 1
    maxy = height + s_radius * 1
    minx = -s_radius * 1
    maxx = width + s_radius * 1


    n = s_radius / s_space
    c = 360 / (rows+2)
    c_step = 0
    for row in range(rows):
        y = (row-2) * s_radius/2
        for col in range(cols):
            x = (col-2) * s_radius/2
            s = Spiral(x, y, s_radius, n, s_space, PI, PI if col%2==0 else 0)
            s.off = 1 if col%2==0 else 0 # is this an offset spiral?
            #s._stroke = (c*c_step, 1, 1)
            if row % 2 == 0:
                spiral_down += [s]
            else:
                spiral_up += [s]
        c_step += 1
    background(0, 0, 0)

def draw():
    noStroke()
    fill(0, 0, 0, 0.15)
    square(0, 0, width)
    
    ymove_speed = sin(QUARTER_PI*frameCount*0.01)
    xmove_speed = cos(QUARTER_PI*frameCount*0.01)
    
    for i, s in enumerate(spiral_down):
        s.move(ymove_speed, -xmove_speed)
        s.draw_me()
    for i, s in enumerate(spiral_up):
        s.move(-ymove_speed, xmove_speed)
        s.draw_me()
    
    saveFrame("frames/#####.png")

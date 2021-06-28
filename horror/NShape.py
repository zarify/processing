from random import uniform, seed, randint, choice
from math import pi

class NShape:
    def __init__(self, sides, sidelen, colour=None, border=False, borderColour=None):
        self.sides = sides if sides >= 3 else 3
        self.sidelen = sidelen if sidelen > 0 else 1
        
        if colour == None:
            self.colour = (randint(50, 200), randint(50, 200), randint(50, 200), randint(50, 200))
        else:
            self.colour = colour
        
        self.border = border
        if borderColour == None:
            self.borderColour = (randint(50, 200), randint(50, 200), randint(50, 200))
        else:
            self.borderColour = borderColour
        
        self.vertices = []
        # Calculate the radius of the shape by using interior triangles
        int_angle = radians(360 / self.sides)
        r = (self.sidelen / 2) / sin(int_angle / 2)
        # Calculate each vertex of the shape
        # from https://stackoverflow.com/questions/7198144/how-to-draw-a-n-sided-regular-polygon-in-cartesian-coordinates
        for i in range(0,sides+1):
            px = r * cos(2 * pi * i / sides)
            py = r * sin(2 * pi * i / sides)
            self.vertices.append((px, py))
    
    def deform(self, iterations, variance, stretchx=1, stretchy=1):
        for i in range(iterations):
            for j in range(len(self.vertices)-1, 0, -1):
                midpoint = ((self.vertices[j-1][0] + self.vertices[j][0])/2 + uniform(-variance, variance)*stretchx,
                            (self.vertices[j-1][1] + self.vertices[j][1])/2 + uniform(-variance, variance)*stretchy)
                self.vertices.insert(j, midpoint)
    
    def getBounds(self):
        minx = int(min([p[0] for p in self.vertices]))
        maxx = int(max([p[0] for p in self.vertices]))
        miny = int(min([p[1] for p in self.vertices]))
        maxy = int(max([p[1] for p in self.vertices]))
        rangex = int(abs(maxx - minx))+1
        rangey = int(abs(maxy - miny))+1
        
        return (minx, miny, rangex, rangey)
    
    def drawShape(self, x, y, blur=0, blended=0, bigger=True):
        minx, miny, rangex, rangey = self.getBounds()
        
        if bigger:
            pad = blur * 2
        else:
            pad = 0
        
        s = createGraphics(rangex + 2*pad, rangey+2*pad)
        s.beginDraw()
        s.colorMode(HSB, 360, 1, 1, 1)
        s.beginShape()
        s.fill(*self.colour)
        
        if self.border:
            s.strokeWeight = self.border
            s.stroke = self.borderColour
        else:
            s.noStroke()
            
        for p in self.vertices:
            s.vertex(p[0] - minx + pad, p[1] - miny + pad)
        s.endShape()
        
        if blur:
            s.filter(BLUR, blur)
        s.endDraw()
        if blended:
            if blended:
                t = blended
            else:
                t = choice([BLEND, ADD, SUBTRACT, DARKEST, LIGHTEST, DIFFERENCE, EXCLUSION, MULTIPLY, SCREEN, OVERLAY,
                            HARD_LIGHT, SOFT_LIGHT, DODGE, BURN])
            blend(s, 0, 0, rangex+2*pad, rangey+2*pad, int(minx-pad+x), int(miny-pad+y), rangex+2*pad, rangey+2*pad, t)
        else:
            image(s, int(minx + x), int(miny + y), rangex, rangey)

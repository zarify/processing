# small areas of symmetry

from random import choice

class Flower: # make a bunch of petals without symmetry
    def __init__(self, x, y, _scale=1.0):
        self.x = x
        self.y = y
        self._scale = _scale
        self.center = random(5,10) * _scale
        self.petals = []
        self.mid_colour = (0, 0, 1)
        self.petal_colour = choice(((51, 0.78, 0.95), (61, 0.85, 0.98), (283, 0.39, 0.86), (313, 0.39, 0.93)))
        
        num_petals = int(random(8,12))
        p_a = TWO_PI/num_petals
        for i in range(num_petals):
            pr = random(20,30)*_scale # this petal radius
            p = [(x,y),(x,y)]
            d1 = random(pr*0.5, pr*0.8)
            d2 = random(pr*0.5, pr*0.8)
            p += [(cos(i*p_a-p_a/2)*d1+x, sin(i*p_a-p_a/2)*d1+y)]
            p += [(cos(i*p_a)*pr+x, sin(i*p_a)*pr+y)] # mid point
            p += [(cos(i*p_a+p_a/2)*d2+x, sin(i*p_a+p_a/2)*d2+y)]
            p += [(x,y),(x,y)]
            self.petals.append(p)
            
    
    def draw_me(self):
        fill(*self.petal_colour)
        for petal in self.petals:
            beginShape()
            for p in petal:
                curveVertex(*p)
            endShape()
        fill(*self.mid_colour)
        circle(self.x, self.y, self.center)

class Butterfly:
    def __init__(self, x, y, _scale=1.0):
        self.x = x # center point
        self.y = y
        self._scale = _scale
        self.r1 = random(5, 10) * _scale # make some randomness in this too?
        self.p1 = [self.r1, -self.r1] # center of top point
        self.r2 = random(8, 14) * _scale
        self.p2 = [self.r2, self.r2] # center of bottom point
        
        self.bodywidth = 0
        self.wing_top = [] # function, (params), fill, stroke, strokeweight e.g. [circle, (xoff, yoff, radius), (0, 1, 1), None]
        self.wing_bottom = []
        self.body = []
        self.feelers = []
    
    def drawPoly(self, points):
        beginShape()
        for x, y in points:
            curveVertex(x, y)
        endShape(CLOSE)
    
    def gen_wings(self):
        # overlay a few polygons over each other slightly deformed and transformed instead
        # polygon method
        h = random(360)
        mod1, mod2, mod3 = random(5,10), random(10,20), random(5,20)
        ymod1, ymod2, ymod3 = random(5,10), random(5,10), random(5,10)
        
        bmod1, bmod2, bmod3 = random(5,15), random(12,30), random(25)
        bymod1, bymod2, bymod3 = random(5,10), random(5,10), random(5,10)
        for xmult in [1,-1]:
            topanchor = (self.x+self.bodywidth/2*xmult, self.y + self.r1*0.25)
            midanchor = (self.x+self.bodywidth/2*xmult, self.y)
            bottomanchor = (self.x+self.bodywidth/2*xmult, self.y)
            
            for i in range(4):
                # top wing
                p = [topanchor, topanchor]
                tr = [self.x + (self.r1 + mod1*i)*xmult, self.y - self.r1 - ymod1*i]
                tr1 = [self.x + (self.r1 + mod2*i)*xmult, self.y - self.r1*0.8 - ymod2*i]
                tr2 = [self.x + (self.r1 + mod3*i)*xmult, self.y + self.r1*2 - ymod3*i]
                p += [tr, tr1, tr2]
                p += [midanchor, midanchor]
                self.wing_top.append([self.drawPoly, [p], (h, 0.8, 0.6, 1), None, None])
                
                # bottom wing
                b = [midanchor, midanchor]
                br = [self.x + (self.r2 + bmod1*i)*xmult, self.y + self.r2]
                br1 = [self.x + (self.r2 + bmod2*i)*xmult, self.y + self.r2*1.2]
                br2 = [self.x + (self.r2 + bmod3*i)*xmult, self.y + self.r2*1.6]
                b += [br, br1, br2]
                b += [bottomanchor, bottomanchor]
                self.wing_bottom.append([self.drawPoly, [b], (h, 0.8, 0.6, 1), None, None])
        
        # circle method
        h = random(360)
        for i in range(50):
            h = 150
            pa = random(TWO_PI) # angle around the center point
            pr = random(self.r1) # distance from center point
            prr = (2 + random(5)) # radius of circle
            for xmult in [1,-1]:
                px = (cos(pa) * pr + self.p1[0]) * xmult + self.x
                py = self.y + self.p1[1]/2.0 - sin(pa) * pr
                self.wing_top.append([circle,
                                    (px, py, prr),
                                    (h, 0.8, 0.6, 1),
                                    None, None])
            h = 0
            pa = random(TWO_PI) # angle around the center point
            pr = random(self.r2) # distance from center point
            prr = (5 + random(5))
            for xmult in [1,-1]:
                
                px = (cos(pa) * pr + self.p2[0]) * xmult + self.x
                py = sin(pa) * pr + self.y + self.p2[1]
                self.wing_bottom.append([circle,
                                    (px, py, prr),
                                    (h, 0.8, 0.6, 1),
                                    None, None])
    
    def gen_body(self):
        _h = self.r1 + self.r2
        _w = random(2,4)*self._scale
        self.bodywidth = _w
        for i in range(5):
            h = choice((0, 37, 57, 124, 282))
            self.body = [[rect,
                        (self.x - _w/2.0, self.y - self.r1, _w, _h, _w*0.75),
                        (h, 0.7, 0.8, 1),
                        None,
                        None]]
        # random bands
        

    def gen_feelers(self):
        lastx, lasty = 0, self.body[0][1][1]
        self.feelers += [(lastx, lasty), (lastx, lasty)]
        
        for s in range(int(random(4,8))): # number of segments
            nextx, nexty = lastx + random(3,6), lasty - random(-4,6)
            self.feelers.append((nextx, nexty))
            lastx, lasty = nextx, nexty
        self.feelers.append((lastx, lasty))
    
    def draw_me(self):
        features = 0
        for f, p, c, s, sw in self.wing_top + self.wing_bottom:
            pushStyle()
            if features > 0:
                blendMode(MULTIPLY)
            if s:
                stroke(*s)
                strokeWeight(sw)
            else:
                noStroke()
            if c:
                fill(*c)
            else:
                noFill()
            f(*p)
            popStyle()
            features += 1
        
        pushStyle()
        noFill()
        stroke(0,0,0,0.5)
        strokeWeight(2)
        for xmult in [1,-1]:
            beginShape()
            for x,y in self.feelers:
                curveVertex(x*xmult + self.x, y)
            endShape()
        popStyle()
        
        for f, p, c, s, sw in self.body:
            pushStyle()
            fill(*c)
            if s:
                stroke(*s)
                strokeWeight(1)
            else:
                noStroke()
            f(*p)
            popStyle()
        

def setup():
    size(800, 800)
    colorMode(HSB, 360, 1, 1, 1)
    background(0,0,1)
    noLoop()
    #randomSeed(42)

def draw():
    for i in range(70):
        r = random(200, width/2-50)
        a = random(TWO_PI)
        x, y = cos(a)*r+width/2, sin(a)*r+height/2
        f = Flower(x, y, _scale=random(1,2))
        f.draw_me()
        
    b = Butterfly(width/2, height/2, _scale=3)
    b.gen_body()
    b.gen_wings()
    b.gen_feelers()
    b.draw_me()
    
    saveFrame("Day_04.png")

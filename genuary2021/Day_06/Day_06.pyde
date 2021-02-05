# triangle subdivision
# draw a triangle, spear it with another triangle at it's mid point, then split
# into smaller triangles

from random import choice

triangles = []
tri_hue = 200
tri_sat = 0.8
tri_bri = 0.7
tri_alpha = 0.5
tri_line = None

DEBUG = False

class Tri:
    def __init__(self, x, y, r, _col, _stroke, _strokeweight, velocity=0.0):
        self.x = x # center point
        self.y = y # center point
        self.r = r
        self.a = random(TWO_PI) # orientation
        self._colour = _col
        self._stroke = _stroke
        self._strokeweight = _strokeweight
        self.velocity = velocity
        self.target = None
        self.target_point = None
        self.shattering = False
        self.shatter_distance = 0.0
        self.side_points = []
        self.gen_points()
        self.mark_for_delete = False
    
    def shatter(self):
        # break into a series of new triangles
        if self.r < 10:
            self.mark_for_delete = True
            return
        for a in (0, radians(120), radians(240)):
            x = cos(self.a + a) * self.r/2.0 + self.x
            y = sin(self.a + a) * self.r/2.0 + self.y
            c = self.get_next_colour()
            t = Tri(x, y, self.r/2.0, c, tri_line, 1, velocity=1.0)
            t.orient(self.a + a)
            t.shattering = True
            t.shatter_distance = t.r * random(3,5)
            triangles.append(t)
        self.mark_for_delete = True
    
    def orient(self, a):
        # orient towards another triangle
        self.a = a
        self.gen_points()
    
    def gen_points(self):
        self.side_points = []
        vh = self.r * sin(radians(30))
        for i in range(3):
            sx = cos(i*radians(120)+self.a+PI)*vh
            sy = sin(i*radians(120)+self.a+PI)*vh
            offset = i * radians(120)
            self.side_points.append((sx+self.x, sy+self.y, offset))
    
    def project(self, distance):
        # pick a random side point
        # project a random distance a 90 degrees from it
        sx, sy, offset = choice(self.side_points)
        d = random(distance-100,distance+100)
        px = cos(self.a + offset) * d + sx
        py = sin(self.a + offset) * d + sy
        self.target_point = [sx, sy]
        return px, py, (offset+self.a+PI)%TWO_PI

    def target_triangle(self, t):
        self.target = t

    def move(self):
        if not self.target and not self.shattering:
            return
        if self.x < 0 or self.x > width or self.y < 0 or self.y > height:
            self.mark_for_delete = True
            if self.target:
                self.target.shatter()
        # move along the projection vector
        px = cos(self.a)*self.velocity+self.x
        py = sin(self.a)*self.velocity+self.y
        if self.target:
            self.x, self.y = px, py
            # calculate 'nose' point and see if it is close enough to target to shatter
            nx = cos(self.a)*self.r+self.x
            ny = sin(self.a)*self.r+self.y
            tx, ty = self.target.target_point
            d = PVector(nx, ny).dist(PVector(tx, ty))
            if d < 1:
                self.velocity = 0.0
                self.shatter()
                self.target.shatter()
                self.target = None
        elif self.shattering:
            d = PVector(px, py).dist(PVector(self.x, self.y))
            self.shatter_distance -= d
            self.x, self.y = px, py
            if self.shatter_distance < 1:
                self.shattering = False
                # now generate a new intersecting triangle for this one
                self.gen_points()
                x, y, a = self.project(self.r*random(2,3))
                t = Tri(x, y, self.r, self._colour, tri_line, 1, velocity=random(0.5,1.5))
                t.orient(a)
                t.target_triangle(self)
                triangles.append(t)
    
    def get_next_colour(self):
        # get the next warmest colour from this triangle's
        h = self._colour[0] - 40
        return (h, tri_sat, tri_bri, tri_alpha)
    
    def draw_me(self):
        x, y = cos(self.a) * self.r + self.x, sin(self.a) * self.r + self.y
        pushStyle()
        fill(*self._colour)
        if self._stroke:
            stroke(*self._stroke)
            strokeWeight(self._strokeweight)
        else:
            noStroke()
        beginShape()
        for i in range(3):
            x, y = cos(self.a + i*radians(120)) * self.r + self.x, sin(self.a + i*radians(120)) * self.r + self.y
            vertex(x, y)
        endShape(CLOSE)
        stroke(0)
        if self.target and DEBUG:
            pushStyle()
            stroke(0)
            line(self.x, self.y, self.target.target_point[0], self.target.target_point[1])
            stroke(100, 1, 1)
            line(self.x, self.y, self.target.x, self.target.y)
            popStyle()
        if self.shattering and DEBUG:
            pushStyle()
            stroke(0, 1, 1)
            tx, ty = cos(self.a)*self.shatter_distance+self.x, sin(self.a)*self.shatter_distance+self.y
            line(self.x, self.y, tx, ty)
            popStyle()
        popStyle()

def setup():
    size(800, 800)
    colorMode(HSB, 360, 1, 1, 1)
    
    t = Tri(400, 400, 100, (tri_hue, tri_sat, tri_bri, tri_alpha), tri_line, 1)
    triangles.append(t)
    x, y, a = t.project(350)
    t2 = Tri(x, y, 100, (tri_hue, tri_sat, tri_bri, tri_alpha), tri_line, 1, velocity=1.5)
    t2.orient(a)
    t2.target_triangle(t)
    triangles.append(t2)
    
    #frameRate(20)

def draw():
    background(0, 0, 0)
    
    for t in triangles:
        t.move()
        t.draw_me()
    
    for i in range(len(triangles))[::-1]:
        if triangles[i].mark_for_delete:
            del triangles[i]
    
    if len(triangles) <= 1:
        noLoop()
    else:
        saveFrame("/Users/rob/tmp/frames/#####.png")

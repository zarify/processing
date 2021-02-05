# polar baton
# each ball has energy which determines which way it spins
# the whole thing has sideways and vertical momentum

from random import choice

cols = (
        [43,.74,.66],
        [27,.87,.67],
        [12,.76,.61]
    )

forces = []
batons = []

paused = False
DEBUG = False
recording = True

cellsize = 100

max_force = 20.0
force_col = lambda x: int((x/max_force)*3)
msgs = ("POW!", "BOOM!", "KA-POW!", "BAM!", "WHACK!", "KER-SPLAT!", "PEW! PEW! PEW!")

class Force:
    def __init__(self, x, y, r):
        self.x, self.y = x, y
        self.r = r
        self.col = cols[force_col(r)]
        self.impacts = 0
        self.mag = r * 10.0
        self.energy = 0 # build up from incoming batons
        self.exploding = False
        self.marked_for_death = False
        self.splosion_points = int(random(9, 15))
        self.splosion_text = choice(msgs)
    
    def draw_me(self):
        if not self.exploding:
            pushStyle()
            noStroke()
            fill(*(self.col + [0.1]))
            circle(self.x, self.y, self.mag)
            fill(*self.col)
            circle(self.x, self.y, self.r)
            popStyle()
        else:
            pushStyle()
            a = 0
            a_off = TWO_PI/41
            
            points = self.splosion_points if self.splosion_points % 2 == 1 else (self.splosion_points + 1)
            a_off = TWO_PI / self.splosion_points / 2
            # shadow
            fill(0)
            beginShape()
            for i in range(points*2):
                x = cos(i*a_off) * self.mag * (1 if i % 2 == 0 else 0.7) + self.x + 3
                y = sin(i*a_off) * self.mag * (1 if i % 2 == 0 else 0.7) + self.y + 3
                vertex(x, y)
            endShape(CLOSE)
            # explosion callout
            stroke(*(self.col))
            fill(*(self.col))
            beginShape()
            for i in range(points*2):
                x = cos(i*a_off) * self.mag * (1 if i % 2 == 0 else 0.7) + self.x
                y = sin(i*a_off) * self.mag * (1 if i % 2 == 0 else 0.7) + self.y
                vertex(x, y)
            endShape(CLOSE)
            
            stroke(0)
            textAlign(CENTER, CENTER)
            
            textSize(40)
            fill(0)
            text(self.splosion_text, self.x+3, self.y+3)
            fill(0,0,1)
            text(self.splosion_text, self.x, self.y)
            popStyle()
            # check for batons in range and push them away
            for b in batons:
                d = PVector(self.x, self.y).dist(PVector(b.x, b.y))
                if d <= self.r:
                    uv = PVector(b.x - self.x, b.y - self.y).normalize()
                    b.v[0] += uv.x
                    b.v[1] += uv.y
            self.r += 6
            if self.r >= self.mag:
                self.marked_for_death = True
            
    
    def check_energy(self):
        if self.energy > 0.9 and not self.exploding:
            self.exploding = True

class End:
    def __init__(self, x, y, r, parent, col, id):
        self.x, self.y = x, y
        self.r = r
        self.parent = parent
        self.col = col
        self.id = id
        self.nx, self.ny = self.x, self.y
    
    def draw_me(self):
        pushStyle()
        fill(*self.col)
        noStroke()
        circle(self.x, self.y, self.r)
        popStyle()
    
    def check_forces(self):
        # check proximity of all forces within their mag radius
        for f in forces:
            d = PVector(self.x, self.y).dist(PVector(f.x, f.y))
            if d <= f.mag/2:
                # check if we're at the min distance (dist between parent and the force center, minus half the length of the parent line)
                min_dist = PVector(self.parent.x, self.parent.y).dist(PVector(f.x, f.y)) - self.parent.l/2.0
                # now check the percentage of the force by using the f.mag as the min amount
                max_dist = f.mag
                applied = ((max_dist - d) / f.mag) * 0.002
                # otherwise check what side of the min distance we're on to determine if it's a CW or CCW force
                a_b = PVector(0, 0).angleBetween(PVector(self.x - self.parent.x, self.y - self.parent.y), PVector(f.x - self.x, f.y - self.y))
                # project the next angle and see if it would increase or decrease to determine which way to push!
                nd = PVector(self.nx, self.ny).dist(PVector(f.x, f.y))
                
                if nd > d: # moving inwards
                    self.parent.a += (-applied if self.parent.a < 0 else applied)
                    # add some momentum away from the force
                    self.parent.v[0] += (-applied if self.parent.a < 0 else applied) # seems to work!
                    f.energy += applied * 3
                else: # moving outwards
                    self.parent.a += (applied if self.parent.a < 0 else -applied)
                
                if DEBUG:
                    pushStyle()
                    noFill()
                    stroke(0)
                    triangle(self.x, self.y, self.parent.x, self.parent.y, f.x, f.y)
                    popStyle()
                
                # then return the force applied back to the baton

class Baton:
    def __init__(self, x, y, l):
        self.x, self.y = x, y
        self.l = l # length
        self.v = [0, random(0.25, 0.75)] # x/y speed
        self.a = radians(random(0.5, 1)) # rotation speed
        if random(1) > 0.5:
            self.a *= -1
        self.angle = random(TWO_PI)# current angle
        self.ends = (End(x-l/2.0, y, random(10,25), self, (197,.37,.24), "E1"),
                     End(x+l/2.0, y, random(10,25), self, (173,.58,.39), "E2"))
        self.marked_for_death = False
    
    def draw_me(self):
        pushStyle()
        stroke(0)
        strokeWeight(2)
        line(self.ends[0].x, self.ends[0].y, self.ends[1].x, self.ends[1].y)
        popStyle()
        self.ends[0].draw_me()
        self.ends[1].draw_me()
    
    def rot(self):
        self.angle += self.a
        e1 = cos(self.angle)*self.l/2.0 + self.x, sin(self.angle)*self.l/2.0 + self.y
        e2 = cos(self.angle+PI)*self.l/2.0 + self.x, sin(self.angle+PI)*self.l/2.0 + self.y
        self.ends[0].x, self.ends[0].y = e1[0], e1[1]
        self.ends[1].x, self.ends[1].y = e2[0], e2[1]
        # now sim the next step and tell each end where it will be next
        na = self.angle + self.a
        e1 = cos(na)*self.l/2.0 + self.x, sin(na)*self.l/2.0 + self.y
        e2 = cos(na+PI)*self.l/2.0 + self.x, sin(na+PI)*self.l/2.0 + self.y
        self.ends[0].nx, self.ends[0].ny = e1[0], e1[1]
        self.ends[1].nx, self.ends[1].ny = e2[0], e2[1]
    
    def move(self):
        self.x += self.v[0]
        self.y += self.v[1]
        # decay any upward movement
        if self.v[1] < 0.75:
            self.v[1] += 0.1
        # bounce off the edges
        if (self.x - self.l/2) < 0 or (self.x + self.l/2) > width:
            self.v[0] *= -1
        # mark for destruction after falling off the bottom
        if (self.y - self.l/2) > height:
            self.marked_for_death = True
        # now check for any proximal forces which might affect movement or rotation
        self.update_forces()
    
    def update_forces(self):
        # ends check proximity to to Forces and return angle adjustments
        # and any movement vector changes
        # need to check for CW/CCW rotation and which direction the end is influencing
        self.ends[0].check_forces()
        self.ends[1].check_forces()

def setup():
    size(1000, 1000)
    colorMode(HSB, 360, 1, 1, 1)
    #f = loadFont("comicz.ttf")
    f = createFont("comicz.ttf", 60)
    textFont(f)
    randomSeed(42)
    global batons, forces
    
    for i in range(10):
        batons.append(Baton(random(100, width-100), random(-100, width/2), random(50, 150)))
    
    cells = width/cellsize
    for y in range(cells):
        for x in range(cells):
            if random(1) > 0.5:
                forces.append(Force(x*cellsize+cellsize/2, y*cellsize+cellsize/2, random(3, 19)))

def draw():
    background(0, 0, 1)

    for f in forces:
        f.draw_me()
        f.check_energy()
    for b in batons:
        b.rot()
        b.move()
        b.draw_me()
    
    
    for i in range(len(batons))[::-1]:
        if batons[i].marked_for_death:
            del batons[i]
            batons.append(Baton(random(100, width-100), -100, random(50, 150)))
    for i in range(len(forces))[::-1]:
        if forces[i].marked_for_death:
            del forces[i]
    
    if recording:
        saveFrame("d:/tmp/frames/batons/#####.png")
        #saveFrame("/Users/rob/tmp/frames/batons#####.png")
    if frameCount > 3000:
        noLoop()
        print("Done")

def mouseClicked():
    global paused
    if not paused:
        noLoop()
        paused = True
    else:
        loop()
        paused = False

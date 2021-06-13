"""
Draw a black and white shape in a separate image object (or take an external image as a source)
and use the colours and positions to determine where things can be drawn, but less precisely than
a mask.

Use a flow field for directional movement. When a mover is outside of the bounds of the masking shape,
decay and respawn if it totally decays. Mask path should continuously regen the strength of the mover.
"""

from random import choice

canvas_width, canvas_height = 2000, 2000
maxframes = 3000
minradius = 0.05 # minimum radius of a mover before it is despawned

concurrentpaths = 200
glowfactor = 3
pathradius = 2.5
decayfactor = 0.9
# ignore the original size limit when increasing radius by travelling in a black area
# not my original idea, but it looks AMAZING
nolimit = True 

noisefactor = 0.03
noise_octaves, falloff = 4, 0.5

colours = (
    (0, 0.8, 0.8),
    (220, 0.8, 0.8),
    (49, 0.91, 0.72),
           # (29, 0.39, 0.8),
           # (72, 0.47, 0.8),
           # (116, 0.39, 0.8),
           # (172, 0.18, 0.8),
           # (332, 0.17, 0.8),
           )

grid = {}
vectors = []

class Mover:
    def __init__(self, x, y, c, r = 2, glow=False):
        self.x, self.y = x, y
        self.c = color(*c)
        self.r = random(r*0.8, r*1.2)
        self.glow = glow
        self.marked = False
    
    def drawMe(self):
        pushStyle()
        fill(self.c)
        noStroke()
        circle(self.x, self.y, self.r)
        if self.glow:
            blendMode(SCREEN)
            circle(self.x, self.y, self.r * glowfactor)
            blendMode(BLEND)
        popStyle()
    
    def moveMe(self):
        steplength = self.r/2.0
        c = round((self.x - left_x) / resolution)
        r = round((self.y - top_y) / resolution)
        try:
            angle = grid[c][r]
        except KeyError:
            # should really kill this off and spawn a new one
            return
        self.x += cos(angle) * steplength
        self.y += sin(angle) * steplength
        
        if not checkCoord(self.x, self.y):
            self.r *= decayfactor
            if self.r <= minradius: # mark this for deletion
                self.marked = True
        else:
            if nolimit or self.r <= pathradius:
                self.r /= decayfactor

def getMask(fn = None):
    if fn:
        img = loadImage(fn)
    else:
        img = createGraphics(width, height)
        img.beginDraw()
        img.colorMode(HSB, 360, 1, 1, 1)
        img.background(0, 0, 1)
        img.strokeWeight(20)
        img.fill(0)
        img.noFill()
        for i in range(8):
            img.circle(random(width*0.1, width*0.9), random(height*0.1, height*0.9), random(width*0.1, width*0.3))
        img.endDraw()
    return img

def checkCoord(x, y):
    x, y = int(x), int(y)
    try:
        p = masker.pixels[y*width + x]
    except:
        return False
    h, s, b = hue(p), saturation(p), brightness(p)
    return s < 0.1 and b < 0.1

def getStarter():
    """
    Load up the masker image and find a random point which is black.
    Return the coordinates.
    """
    masker.loadPixels()
    while True:
        x, y = int(random(width)), int(random(height))
        p = masker.pixels[y*width + x]
        h, s, b = hue(p), saturation(p), brightness(p)
        if b < 0.1 and s < 0.1:
            break
    return x, y

def setup():
    global masker
    size(canvas_width, canvas_height)
    colorMode(HSB, 360, 1, 1, 1)
    
    # ------- FLOW FIELD SETUP
    global left_x, right_x, top_y, bottom_y, resolution, res_factor
    left_x = int(width * -0.5)
    right_x = int(width * 1.5)
    top_y = int(height * -0.5)
    bottom_y = int(height * 1.5)
    res_factor = 0.005
    # path grid
    resolution = int(width * res_factor)
    num_columns = (right_x - left_x) / resolution
    num_rows = (bottom_y - top_y) / resolution
    
    frameRate(30)
    background(0, 0, 0.2)
    
    q1 = q2 = q3 = q4 = 0
    
    noiseDetail(noise_octaves, falloff)
    
    for c in range(num_columns):
        grid[c] = {}
        for r in range(num_rows):
            #angle = ((r+c) / float(num_rows+num_columns) * PI)
            angle = noise(c * noisefactor, r * noisefactor) * TWO_PI * 2
            #angle = (r + c) * 0.01 % TWO_PI
            #angle = sin(r + c)
            
            grid[c][r] = angle
            
            if angle >= 0 and angle <= HALF_PI:
                q1 += 1
            elif angle < PI:
                q2 += 1
            elif angle < (PI + HALF_PI):
                q3 += 1
            elif angle < TWO_PI:
                q4 += 1
    total = float(q1 + q2 + q3 + q4)
    print("q1: {:.2f}\nq2 {:.2f}\nq3 {:.2f}\nq4 {:.2f}".format(q1/total, q2/total, q3/total, q4/total))
    
    masker = getMask("ring_of_fire.png")
    
    
    # --------- MOVEMENT AGENT SETUP
    for i in range(concurrentpaths):
        x, y = getStarter()
        vectors.append(Mover(x, y, choice(colours), r=pathradius, glow=True))

    #image(masker, 0, 0)

def draw():
    noStroke()
    
    for i in range(len(vectors)-1,-1,-1):
        vectors[i].drawMe()
        vectors[i].moveMe()
        if vectors[i].marked: # delete this vector and add a new one to the end of the list
            del vectors[i]
            x, y = getStarter()
            vectors.append(Mover(x, y, choice(colours), r=pathradius, glow=True))
    
    if frameCount >= maxframes:
        noLoop()
        print("Done")
        save("constrained.png")

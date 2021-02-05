from random import choice, randint, seed

starters = ((31, .88, .7), (106, .83, .57), (147, .65, .61), (169, .91, .65), (216, .91, .65), (253, .78, .71), (296, .88, .72), (316, .65, .63))
tints = ((0, .7, .9), (202, .84, .92), (155, .84, .92))
modes = (ADD, DIFFERENCE, EXCLUSION, MULTIPLY, SCREEN)

def marble(x, y, r, c, recurse=False):
    pushMatrix()
    pushStyle()
    translate(x, y)
    if recurse:
        blendMode(BLEND)
    else:
        blendMode(choice(modes))
        
    fill(*c)
    circle(0, 0, r)
    popStyle()
    popMatrix()
    if recurse:
        for i in range(1,4)[::-1]:
            marble(x+random(-2, 2), y+random(-2,2), r*i/4.0, c)
    
def highlight(x, y, r):
    pushMatrix()
    pushStyle()
    translate(x, y)
    blendMode(SCREEN)
    fill(0, 0, 1, 0.5)
    circle(-r/5, -r/5, r/3)
    popStyle()
    popMatrix()

def curve_shape(c):
    pushStyle()
    tl_x, tl_y = random(15, 50), random(15, 50)
    
    vertices = ((random(width*.25, width*0.75), random(15, 50), random(-10, -100), random(-10, 10)), # top mid
                 (random(width-50, width-15), random(10, 50), random(-10, -50), random(-20, -40)), # top right
                 (random(width*0.8, width-15), random(height*0.4, height*0.6), 0, random(-100, -200)), # right mid
                 (random(width-50, width-10), random(height-50, height-15), random(20, 30), random(20, 50)), # bottom right
                 (random(width*.4, width*.6), random(height-50, height-15), random(50, 100), random(-10, -50)), # bottom mid
                 (random(10, 50), random(height-50, height-15), random(-5, 0), random(10, 30)), # bottom left
                 (random(10, 100), random(height*.25, height*.75), 0, random(50, 100)), # left mid
                 (tl_x, tl_y, random(-15,-20), 0) # top left
                 )

    fill(*c)
    
    for bm, offset in ((BLEND, (0,0)),
                       (SUBTRACT, (random(5,10), random(5,10)))
                       ):
        blendMode(bm)
        beginShape()
        vertex(tl_x + offset[0], tl_y + offset[1])
        
        for x, y, mx, my in vertices:
            # calculate some control points
            cx = x + mx + offset[0]
            cy = y + my + offset[1]
            quadraticVertex(cx, cy, x + offset[0], y + offset[1])
    
        endShape(CLOSE)
    
    popStyle()

def setup():
    size(800, 800)
    colorMode(HSB, 360, 1, 1, 1)
    noLoop()
    noStroke()
    
    s = int(random(100000))
    print(s)
    randomSeed(s)
    seed(s)

def draw():
    #background(0, 0, 0.3)
    # border
    fill(0, 0, 1)
    stroke(0)
    strokeWeight(10)
    rect(0, 0, width, height)
    noStroke()
    
    # draw a nice curved shape in the background
    c = list(choice(starters))+[0.6]
    c[1] = 0.3
    c[2] = 0.15
    curve_shape(c)
    
    # draw some marbles
    for i in range(300+int(random(300))):
        r = random(20, 50)
        x, y = random(r, width-r), random(r, height-r)
        c = choice(starters)
        marble(x, y, r, c, recurse=True)
        highlight(x, y, r)
    
    saveFrame("marbles.png")

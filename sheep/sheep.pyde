from random import randint, choice, seed

w, h = 1000, 1000
sheep_size = 90
grid = int(w / sheep_size
           )
#        purple          blue            grey             orange
cols = ((148, 29, 198), (29, 145, 198), (200, 200, 200), (234, 145, 21))

def sheep_head(x, y, features=False):
    pushStyle()
    # head
    arc(x, y, 30, 50, 0, PI, OPEN) # lower part
    arc(x, y-1, 35, 30, PI+PI/5, PI+4*PI/5, OPEN) # top part
    arc(x-15, y-5, 15, 10, PI/2, PI+PI/2, OPEN) # left ear
    arc(x+15, y-5, 15, 10, PI+PI/2, 2*PI+PI/2, OPEN) # right ear
    if features:
        # eyes
        strokeWeight(3)
        strokeCap(ROUND)
        point(x-8, y-2)
        point(x+8, y-2)
        strokeWeight(1)
        # nose
        arc(x, y+10, 7, 11, PI/4, 3*PI/4, OPEN)
        # mouth
        arc(x, y+10, 13, 18, PI/4, 3*PI/4, OPEN)
        # bridge
        line(x-0.5, y+14, x, y+17)
    popStyle()

def sheep_feet(x, y):
    # right foot
    beginShape()
    vertex(x + 17, y)
    quadraticVertex(x + 17, y, x + 20, y + 8)
    quadraticVertex(x + 22, y + 8, x + 23, y + 16)
    quadraticVertex(x + 15, y + 22, x + 5, y + 16)
    quadraticVertex(x + 8, y+5, x + 8, y)
    endShape()
    
    # left foot
    beginShape()
    vertex(x - 17, y)
    quadraticVertex(x - 17, y, x - 20, y + 8)
    quadraticVertex(x - 22, y + 8, x - 23, y + 16)
    quadraticVertex(x - 15, y + 22, x - 5, y + 16)
    quadraticVertex(x - 8, y+5, x - 8, y)
    endShape()

def sheep_body(x, y, tail=False, col=(255, 255, 255)):
    pushStyle()
    fill(*col)
    circle(x, y, 50)
    if tail:
        arc(x, y, 10, 15, 0, PI, OPEN)
    popStyle()

def sheep(x, y, c = (255,255,255)):
    # feet, circle, head shape, features
    sheep_feet(x, y+20)
    sheep_body(x, y, col=c)
    sheep_head(x, y-30, features=True)

def backwards_sheep(x, y, c = (255, 255, 255)):
    # feet, head shape, no features, circle then tail
    sheep_feet(x, y+20)
    sheep_head(x, y-30, features=False)
    sheep_body(x, y, tail=True, col=c)

def setup():
    size(w, h)
    background(255, 255, 255)
    
    for y in range(1,grid-2,2):
        for x in range(0, grid+1):
            col = (255, 255, 255)
            if random(100) > 95:
                col = choice(cols)
            if random(100) < 95:
                sheep(x * sheep_size, y * sheep_size, col)
            else:
                backwards_sheep(x * sheep_size, y * sheep_size, col)
            
            col = (255, 255, 255)
            if random(100) > 95:
                col = choice(cols)
            if random(100) < 95:
                sheep((x+0.5) * sheep_size, (y + 1) * sheep_size, col)
            else:
                backwards_sheep((x+0.5) * sheep_size, (y + 1) * sheep_size, col)
    
    # sheep(400, 400)
    # backwards_sheep(500, 400)

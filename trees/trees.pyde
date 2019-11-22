from NShape import NShape
from random import randint, choice, seed

w, h = 500, 500

max_angle = 45
max_branches = 8
leafsize = 20

cols = ((51, 204, 51), (102, 153, 0), (0, 102, 0), (51, 153, 51))
trunk_cols = ((89,63,7), (86,44,6), (104,62,25), (124,92,16), (102, 51, 0))

def leaf(x, y):
    l = NShape(randint(4,8), randint(leafsize//2, leafsize+leafsize//2), choice(cols))
    l.deform(randint(2,5), random(3)+1, stretchx=random(1)+1, stretchy=random(1)+1)
    l.drawShape(x,y)

def branch(x, y, angle, weight, l, branches=0, trunk_col=(102, 51, 0)):
    strokeWeight(weight)
    stroke(*trunk_col)
    
    nx, ny = sin(radians(abs(angle))) * l, cos(radians(abs(angle))) * l
    if angle < 0:
        nx *= -1
    nx = x + nx
    ny = y - ny
    line(x, y, nx, ny)
    
    
    nb = randint(1, 3)
    if branches / max_branches > 0.5: # chance of petering out after halfway there
        if random(100) > 80:
            nb = 0
    if nb == 0 or branches >= max_branches:
        leaf(nx, ny)
    else:
        for i in range(nb):
            a = randint(0, max_angle)
            if randint(0,1):
                a *= -1
            branch(nx, ny, a, weight*0.85, l*randint(5,9)/10, branches+1, trunk_col)

def setup():
    size(w, h)
    background(135, 206, 235)
    
    for i in range(10):
        tc = choice(trunk_cols)
        x = random(400)+50
        thick = random(10)+4
        l = randint(50,100)
        branch(x, h, 0, thick, l, trunk_col=tc)
    save("trees.png")
    

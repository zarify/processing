from gen_grid import generateGrid
from add_noise import random_noise
from colour_set import pick_colour
from click_save import *
from random import choice

def setup():
    size(800, 800)
    colorMode(HSB, 360, 1, 1, 1)

def wriggle(x, y, n, delta=2.0, a_off=0):
    da = TWO_PI / n
    return [(cos(i * da + a_off) * random(delta/2.0, delta) + x, sin(i * da + a_off) * random(delta/2.0, delta) + y) for i in range(n)]

def draw():
    background(0, 0, 1)
    
    cells = generateGrid(cellsize=100, canvasSize=width, buffer=1)
    colours = pick_colour()
    
    strokeWeight(3)
    for x, y in cells:
        if random(1) > 0.5:
            sz = random(60, 90)
            # for wx, wy in wriggle(x, y, 9, delta=9, a_off=random(TWO_PI)):
            #     sx, sy = wx - sz/2.0, wy - sz/2.0
            #     pushStyle()
            #     blendMode(MULTIPLY)
            #     fill(choice((0, 120, 240)), 1, 1, 0.5)
            #     noStroke()
            #     square(sx, sy, sz)
            #     popStyle()
            blendMode(BLEND)
            sx, sy = x - sz/2.0, y - sz/2.0
            fill(*choice(colours))
            stroke(*choice(colours))
            square(sx, sy, sz)
    
    # add some noise to some of the squares
    
    noise_colour = choice(colours)
    random_noise(thresh=0.6, amt=0.3, colours=(noise_colour,), similarity=0.2)
    
    for x, y in cells:
        if random(1) > 0.6:
            sz = random(20, 50)
            for wx, wy in wriggle(x, y, 3, delta=8, a_off=random(TWO_PI)):
                pushStyle()
                blendMode(MULTIPLY)
                fill(choice((0, 120, 240)), 1, 1, 0.5)
                noStroke()
                circle(wx, wy, sz)
                popStyle()
            fill(*choice(colours))
            stroke(*choice(colours))       
            circle(x, y, sz)
    
    noLoop()

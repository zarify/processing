from add_noise import *
from click_save import *
from NShape import *
from colour_set import pick_colour
from random import choice

drawHole = True

def setup():
    size(800, 800)
    colorMode(HSB, 360, 1, 1, 1)

def draw():
    background(0, 0, 0)
    colours = pick_colour()
    
    c = list(choice(colours))
    # clouds
    for i in range(100):
        x = width * 0.5 + random(-width * 0.2, width * 0.2)
        y = height * 0.5 + random(-height * 0.2, height * 0.2)
        cloud = NShape(8, random(30, 60), colour=c+[random(0.02, 0.09)])
        sx, sy = random(0.5, 5.5), random(0.5, 5.5)
        for i in range(4):
            cloud.deform(3, 3, stretchx=sx, stretchy=sy)
            cloud.drawShape(x, y, blur=1, blended=BLEND)
    # holes
    for i in range(30):
        x = width * 0.5 + random(-width * 0.2, width * 0.2)
        y = height * 0.5 + random(-height * 0.2, height * 0.2)
        cloud = NShape(8, random(10, 50), colour=[0,0,1]+[random(0.05, 0.1)])
        sx, sy = random(0.5, 8.5), random(0.5, 8.5)
        for i in range(3):
            cloud.deform(3, 4, stretchx=sx, stretchy=sy)
            cloud.drawShape(x, y, blur=1, blended=SUBTRACT)
    
    if drawHole:
        fill(0)
        # main hole
        x, y = width/2, height/2
        hole = NShape(50, 12, colour=(0, 0, 0, 0.5))
        sx, sy = random(0.5, 3.5), random(0.5, 3.5)
        for i in range(3):
            hole.deform(3, 4, stretchx=sx, stretchy=sy)
            hole.drawShape(x, y, blur=1)
    
    print("Done frame")
    noLoop()

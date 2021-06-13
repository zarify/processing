from NShape import NShape
from add_noise import random_noise
from gen_grid import generateGrid
from random import choice

import datetime
import subprocess

layer = 3 # layers of deformed petal shapes
blendlayers = 2 # 1 for BLEND, 2 for random
deformamount = 2 # 0 for random 2, 6
variance_divisor = 35.0

def setup():
    size(800, 800)
    colorMode(HSB, 360, 1, 1, 1)
    frameRate(30)
    print("Starting")

def draw():
    background(0, 0, 1)
    
    cellsize = 800
    h = random(360)
    grid = generateGrid(cellsize, width)
    for x, y in grid:
        r = cellsize
        a = random(TWO_PI)
        while r > (cellsize / 5.0):
            shp = NShape(7, r/4, border=True, borderColour=(h, 0.2, 0.2, 0.2), colour=(h, 0.8, 0.8, 1), curved=True)
            for i in range(layer):
                shp.deform(deformamount if deformamount else int(random(2,6)), r/variance_divisor)
                cx, cy = cos(a) * r/10.0 + x, sin(a) * r/10.0 + y
                shp.drawShape(cx, cy, blur=0, blended=blendlayers)
            r *= random(0.9, 0.95)
            a += random(QUARTER_PI, HALF_PI)
    
    # random_noise(thresh=0.75, amt=0.2, colours=((h, 0.8, 0.8),))
    print("Draw done.")
    noLoop()
    

def mouseClicked(event):
    if event.button == 37: # left
        print("Next...")
        loop()
    elif event.button == 39: # right
        stamp = datetime.datetime.now().replace(microsecond=0).isoformat()
        stamp = stamp.replace(":","-")
        fn = "versions/flower_" + stamp + ".png"
        save(fn)
        print("Saved.")

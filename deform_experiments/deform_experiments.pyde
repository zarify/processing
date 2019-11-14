from random import uniform, seed, randint
from time import time
from math import pi

from NShape import NShape

w, h = 1920, 1080

def setup():
    size(w, h)
    background(0,0,0)
    
    # seed(50)
    # randomSeed(50)

    for i in range(randint(80,150)):
        x = random(w)
        y = random(h)
        s = randint(3,9)
        sz = randint(50,250)
        r, g, b = randint(50, 200), randint(50, 200), randint(50, 200)
        for j in range(1):
            tmp = NShape(s, sz, (r, g, b, 40))
            tmp.deform(randint(3,7), randint(3,8), stretchx=random(5), stretchy=random(5))
            tmp.drawShape(x, y, blur=randint(1,5), blended=randint(0,2))
    save("output_7.png")

# TODO:
# - fewer colours (CW, CCW, CW+, CCW+, thin, thick, colour change)
# - arcs only
# - constant speed

from p5 import *
from random import random, choice
from math import sin, cos, pi, radians

hues = (
           (233,.96,.46), # slight CW
           (128, .96, .46), # slight CCW
           (0, .67, .53), # bigger
           (350, .62, .75), # smaller
           (313, .74, .7), # cycle colours
           (228, .83, .54), # large CW
           (124, .83, .54), # large CCW
           (265, .79, .63) # dupe
           )

movers = []
max_cooldown = 60
dupe_cooldown = max_cooldown
min_width = 4
max_width = 20

class Picker:
    def __init__(self):
        self.x = width/2
        self.y = height/2
        self.w = 50
        self.w_org = self.w
        self.wm = 1
        self.c = choice(hues)

    def pick(self):
        self.c = choice(hues)

    def draw_me(self):
        push_style()
        no_stroke()
        fill(0,0,1)
        circle(self.x, self.y, self.w_org+12)
        fill(*self.c)
        circle(self.x, self.y, self.w)
        self.w += self.wm
        if self.w > (self.w_org + 10) or self.w < (self.w_org - 5):
            self.wm *= -1
        pop_style()

class Mover:
    def __init__(self, x, y, col, v, a):
        self.x = x
        self.px = x # previous x
        self.y = y
        self.py = y
        self.col = col # hsl list
        self.v = v # velocity
        self.a = a # vector angle
        self.w = min_width
    
    def move(self):
        self.px, self.py = self.x, self.y
        self.x = cos(self.a)*self.v + self.x
        self.y = sin(self.a)*self.v + self.y
        if self.x < 0 or self.x > width or self.y < 0 or self.y > height:
            # bounce at a random angle
            if self.x < 0:
                self.a = random()*pi - pi/2
            elif self.x > width:
                self.a = random()*pi + pi/2
            elif self.y < 0:
                self.a = random()*pi
            elif self.y > height:
                self.a = random()*pi + pi
            # move to contact
            if self.x < 0:
                self.x = 0
            elif self.x > width:
                self.x = width
            if self.y < 0:
                self.y = 0
            elif self.y > height:
                self.y = height
        
        self.update()
    
    def update(self):
        global dupe_cooldown
        i = hues.index(picker.c)
        if i == 0:
            self.a += radians(random())
        elif i == 1:
            self.a -= radians(random())
        elif i == 2:
            if self.w <= max_width:
                self.w += random()*0.1
            else:
                return 1
        elif i == 3:
            if self.w >= min_width:
                self.w -= random()*0.1
            else:
                return 1
        elif i == 4:
            self.col[0] = (self.col[0] + 1) % 360
        elif i == 5:
            self.a += radians(random()*3)
        elif i == 6:
            self.a -= radians(random()*3)
        elif i == 7:
            if dupe_cooldown == 0:
                movers.append(Mover(width/2, height/2, [0,0.7,0.8], 4, random()*pi*2))
                dupe_cooldown = max_cooldown
        return 0
    
    def draw_me(self):
        push_style()
        stroke(*self.col)
        stroke_weight(self.w)
        line((self.px, self.py), (self.x, self.y))
        pop_style()

def setup():
    global root, picker
    size(800, 800)
    color_mode('HSB', 360, 1, 1, 1)
    movers.append(Mover(width/2, height/2, [0,0.7,0.8], 4, random()*pi*2))
    picker = Picker()
    
def draw():
    global dupe_cooldown
    if frame_count == 1:
        background(0, 0, 0)
    if frame_count % 10 == 0:
        push_style()
        no_stroke()
        fill(0, 0, 0, 0.1)
        square(0, 0, width)
        pop_style()
    if frame_count % 30 == 0:
        if random() > 0.7:
            if picker.pick():
                picker.pick()
    if dupe_cooldown > 0:
        dupe_cooldown -= 1
    
    for mover in movers:
        mover.move()
        mover.draw_me()
    picker.draw_me()
    
    if frame_count < 3000:
        save_frame("frames/#####.png")
        pass
    else:
        no_loop()
        print("Done")

run()
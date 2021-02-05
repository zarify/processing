from p5 import *
from random import random, randint

subdiv_colour = [209, .77, .59]

thresh = 50
max_bounces = 5

class Mover:
    def __init__(self, x, y, col, v, b):
        self.x = x
        self.px = x # previous x
        self.y = y
        self.py = y
        self.col = col # hsl list
        self.v = v # movement vector
        self.bounces = b
    
    def move(self):
        self.px, self.py = self.x, self.y
        self.x += self.v[0]
        self.y += self.v[1]
        push_style()
        no_fill()
        stroke(*subdiv_colour)
        bounced = False
        if self.x <= boundsx[0] or self.x >= boundsx[1]:
            self.bounces -= 1
            self.v[0] *= -1
            # create a horizontal line
#             line((boundsx[0], self.y), (boundsx[1], self.y))
            hlines.append(self.y)
            hlines.sort()
            # modify bounds
            if self.y > boundsy[0]:
                boundsy[0] = self.y
            elif self.y < boundsy[1]:
                boundsy[1] = self.y
            bounced = True
        if self.y <= boundsy[0] or self.y >= boundsy[1]:
            self.bounces -= 1
            self.v[1] *= -1
            # create a vertical line
#             line((self.x, boundsy[0]), (self.x, boundsy[1]))
            vlines.append(self.x)
            vlines.sort()
            # modify bounds
            if self.x > boundsx[0]:
                boundsx[0] = self.x
            elif self.x < boundsx[1]:
                boundsx[1] = self.x
            bounced = True
        pop_style()
        if (boundsx[1] - boundsx[0]) < thresh or (boundsy[1] - boundsy[0]) < thresh or self.bounces < 0:
            self.teleport()
    
    def teleport(self):
        # draw a rect in the current bounding box
        push_style()
        fill(random()*360, 0.7, 0.7)
        rect(boundsx[0], boundsy[0], boundsx[1]-boundsx[0], boundsy[1]-boundsy[0])
        pop_style()
        
        self.x = randint(0,width)
        self.y = randint(0,height)
        self.bounces = randint(2, max_bounces)
        
#         push_style()
#         fill(0, 1, 1)
#         no_stroke()
#         circle(self.x, self.y, 10)
#         pop_style()
        
        self.px, self.py = self.x, self.y
        self.v = [random()*4-2, random()*4-2]
        print(f"Teleported to ({self.x},{self.y}), Bounces: {self.bounces}")
        # recalculate bounds
        for i, x in enumerate(vlines):
            if self.x > x and self.x < vlines[i+1]:
                boundsx[0] = x
                boundsx[1] = vlines[i+1]
                break
        for i, y in enumerate(hlines):
            if self.y > y and self.y < hlines[i+1]:
                boundsy[0] = y
                boundsy[1] = hlines[i+1]
                break
    
    def draw_me(self):
        push_style()
        stroke(*self.col)
        stroke_weight(1.5)
        line((self.px, self.py), (self.x, self.y))
        pop_style()

def setup():
    global root, boundsx, boundsy, vlines, hlines
    size(800, 800)
    color_mode('HSB', 360, 1, 1, 1)
    root = Mover(width/2, height/2, [0,0,0], [random()*4-2, random()*4-2], randint(2, max_bounces))
    boundsx = [0, width]
    boundsy = [0, height]
    vlines, hlines = [0, width], [0, height] # sorted lists of x and y coordinates of lines
    
def draw():
    if frame_count == 1:
        background(0, 0, 1)

    root.move()
    #root.draw_me()

def mouse_clicked():
    no_loop()
    save_frame("d14_bounces.png")
    print("Done")

run()
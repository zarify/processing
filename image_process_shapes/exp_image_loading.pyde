from NShape import NShape
from random import randint, seed

w, h = 1000, 1000
stepsize = 8
maxframes = 10



coords = [] # (x, y, (r,g,b))

def setup():
    size(w, h)
    background(0, 0, 0)
    
    src = loadImage("carton.png")

    noStroke()
    # noLoop()
    
    src.loadPixels()

    # average squares 6x6
    for y in range(0, h, stepsize):
        off = y * w
        for x in range(0, w, stepsize):
            p = []
            reds, blues, greens = 0, 0, 0
            for i in range(stepsize):
                xoff = off + x + i * w
                p += src.pixels[xoff:xoff+stepsize] # main offset + block x val + y strips of block
            reds = sum([red(pix) for pix in p])
            blues = sum([blue(pix) for pix in p])
            greens = sum([green(pix) for pix in p])
            
            # average out the colour of this region
            col = (reds/len(p), greens/len(p), blues/len(p), 80)
            
            coords.append((x, y, col))

def draw():
    if frameCount >= maxframes:
        exit()
    for x, y, col in coords:
        sz = stepsize
        r = random(100)
        if r > 95:
            sz *= 4
        elif r > 85:
            sz *= 2
        s = NShape(randint(3, 6), randint(sz/2,sz+sz/2), colour=col)
        s.deform(2, 5)
        s.drawShape(x, y)
    saveFrame("frames/frame-##.png")

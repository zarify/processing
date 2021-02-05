h = 160
xorg = 0
yoff = 400
xcount = 0
xvel = 2

def setup():
    size(800, 800)
    colorMode(HSB, 360, 1, 1, 1)
    background(140, 0.49, 0.75)
    frameRate(30)
    noStroke()

def draw():
    global h, xorg, yoff, xcount, xvel
    if frameCount % 10 == 0:
        fill(140, 0.49, 0.75, 0.2)
        square(0,0,width)
    pushMatrix()
    translate(xorg,yoff)
    y = sin((frameCount%20)/20.0*PI+PI)*h
    if (frameCount % 20 == 0 and frameCount > 0):
        h -= 50
    if h <= 0:
        fill(0)
        ellipse(xcount, y, 25, 10)
        fill(0,0,1)
        circle(xcount, y, 5)
        yoff = random(300, 700)
        xcount = 0
        xvel = random(1,3)
        if random(1)>0.5:
            xvel *= -1
            xorg = random(400,600)
        else:
            xorg = random(50,400)
        h = int(random(3,7))*50
    else:
        fill(0,0,1)
        circle(xcount, y, 5)
        xcount += xvel
    popMatrix()
    
    saveFrame("frames/####.jpg")
    if frameCount > 700:
        noLoop()

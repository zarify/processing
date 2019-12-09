from random import randint, seed

w, h = 800, 800
maxframes = 2000       # number of frames to animate over
maxvecs = 100          # number of vector paths to have onscreen at once
maxsize = 40           # max repulsor strength
animate = False        # record each frame (~500kb per frame)
DEBUG = False           # draw the repulsor circles if true, otherwise hide them
ignoreDistance = 10    # this makes the pretty halo, even if it was put in to avoid a bug
randColour = True      # vectors choose a random colour rather than being grey

# repulsors want to push stuff away from them
# (x, y, v) where v is a pushing magnitude
reps = []
# vectorss want to get across the screen
# (x, y, v, w, c) where v is the direction vector and x, y is current position, w is the line weight, c is colour
vecs = []

def setup():
    size(w, h)
    colorMode(HSB, 1)
    
    background(0, 0, 1)
    
    
    # frameRate(10)
    
    for i in range(maxvecs):
        c = (0, 0, 0.5, 0.1)
        if randColour:
            c = (random(1), random(1), 0.5, 0.1)
        vecs.append([randint(50, 750), randint(50, 750), PVector(randint(-2,2),randint(-2,2)), random(2), c])
    
    for i in range(40):
        reps.append((randint(0, w), randint(0, h), randint(5, maxsize)))
    
    if DEBUG:
        pushStyle()
        noStroke()
        for r in reps:
            x, y, v = r
            fill(v/25.0, 1.0, 1.0, 0.3)
            circle(x, y, v*1.5)
        popStyle()

def draw():
    global vecs, reps, ignoreDistance
    
    if frameCount == maxframes:
        print("Done.")
        noLoop()
        save("repulsors.png")
    
    # move each vector taking into account proximity of repulsors
    for i in range(len(vecs)):
        x, y, v, w, c = vecs[i]
        applied = [v.x,v.y] # total force applied
        for r in reps: # modify vector according to forces from all repulsors
            newpos = PVector(x + v.x, y + v.y)
            forcepos = PVector(r[0], r[1])
            # distance from r to newpos
            fdist = newpos.dist(forcepos)
            force = r[2] ** (3/((fdist+0.01)/10)) #- 0.9
            if force > ignoreDistance:
                continue
            # use the force as a multiplier for x/y component forces
            try:
                xperc = abs(newpos.x - r[0]) / (abs(newpos.x - r[0]) + abs(newpos.y - r[1]))
            except ZeroDivisionError:
                xperc = 0.0
            try:
                yperc = abs(newpos.y - r[1]) / (abs(newpos.x - r[0]) + abs(newpos.y - r[1]))
            except ZeroDivisionError:
                yperc = 0.0
            xcomp = force * xperc
            ycomp = force * yperc
            if x < r[0]: # point on left of repulsor, -ve x force
                xcomp *= -1
            if y < r[1]:
                ycomp *= -1
            applied[0] += xcomp
            applied[1] += ycomp
        strokeWeight(w)
        stroke(*c)
        line(x, y, x + applied[0], y + applied[1]) # use direction vector to draw line
        vecs[i][0] = x + applied[0] # update position by current vector
        vecs[i][1] = y + applied[1]

    vecs = [v for v in vecs if v[0] >= 0 and v[0] <= w and v[1] >= 0 and v[1] <= h]
    while len(vecs) < maxvecs:
        c = (0, 0, 0.5, 0.1)
        if randColour:
            c = (random(1), random(1), 0.5, 0.1)
        vecs.append([randint(50, 750), randint(50, 750), PVector(randint(-2,2),randint(-2,2)), random(2), c])
    
    if animate:
        saveFrame("frames/repulse_####.png")
        

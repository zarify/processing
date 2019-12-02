from random import randint

shadows = False # shadows under circles, was a nice idea but looks gross
recording = False # save frames for building movie
randomRipples = True # mouse interaction as well as random generation of ripples
mountains = True # whether to add colliding ripple strength together or use max height

density = 160 # how dense the grid is
w, h, = 800, 800
cs = w / density # circle size

ripples = [] # [x, y, distance from epicenter, strength]

circles = [] # [x, y, z, col, p] where p is total ripple influence

for y in range(1,density):
    for x in range(1,density):
        circles.append([x * cs, y * cs, 0, [0, 0, 300], 0])

def ripple():
    for i in range(len(circles)):
        cx, cy, cz, col, p = circles[i]
        p = 0 # reset total ripple influence on this circle
        circles[i][2] = 0 # reset z value at the start of every pass
        circles[i][3] = [0, 0, 300] # reset colour values every pass

        for j in range(len(ripples)):
            rx, ry, rd, rh = ripples[j]
            c_to_r = sqrt((cx - rx)**2 + (cy - ry)**2) # euclidean distance to ripple center
            thresh = rh # how far the ripple affects dependent on how strong it still is
            if c_to_r >= (rd - thresh) and c_to_r <= (rd + thresh): # near enough to matter
                
                perc = 1 - abs(c_to_r - rd) / thresh # percentage of distance threshhold
                z = rh * perc
                p += z # add height to ripple influence (for colour variance)
                
                # add to colour saturation as height increases
                # want this to be additive with other ripples
                circles[i][3][1] = sum((perc * 360, col[1]))
                
                # use the max z value or add together based on config
                if mountains:
                    m = sum
                else:
                    m = max
                circles[i][2] = m([circles[i][2], z])

        circles[i][3][0] = p * 2 # circle colour affected by total ripple interaction
    for j in range(len(ripples)):
        ripples[j][2] += 5
        ripples[j][3] -= 1

def setup():
    size(w, h, P3D)
    colorMode(HSB, 360)
    background(0, 0, 360)
    noStroke()
    frameRate(15)

def draw():
    global shadows, ripples

    background(0, 0, 360)

    if shadows:
        fill(250)
        for x, y, z, _, _ in circles:
            circle(x, y, cs-2)
    
    if randomRipples and random(100) > 95:
        ripples.append([random(w), random(h), 0, randint(10, 60)])
    
    # show ripple effect
    ripple()
    ripples = [r for r in ripples if r[3] > 0]
    
    # circles
    fill(0, 0, 300)
    for x, y, z, col, p in circles:
        translate(0, 0, z)
        fill(*col)
        circle(x, y, cs-2)
        translate(0, 0, -z)
    if recording:
        saveFrame("frames/frame-####.png")

def mouseClicked():
    ripples.append([mouseX, mouseY, 0, randint(10, 60)])

from random import uniform
from random import choice
from random import randint

bg = (50, 50, 50)

def pointOnEllipse(ex, ey, ew, eh, px):
    """
    Return the y coordinate for a given x coordinate (px) on the top half
    of an ellipse with the given x, y, width and height values.
    Position is calculated by finding the x, y position on the greater
    circle, and then using the width/height ratio to shift the y position
    to the correct location.
    """
    ratio = float(eh) / float(ew)
    opp = sqrt((ew/2)**2 - abs(px-ex)**2)
    opp *= ratio
    return ey-opp

def octagon(x, y, side, stretch=1):
    """
    Create and return a list of vertices in an octagon with top-left point
    coordinates x, y, and straight side length 'side'.
    Optional stretch factor for creating wider octagons for cloud shapes.
    """
    d = side / sqrt(2)
    oct = []
    oct.append((x, y)) # top left
    oct.append((x+side*stretch, y)) # top right
    oct.append((x+side*stretch+d, y+d)) # right top
    oct.append((x+side*stretch+d, y+d+side)) # right bottom
    oct.append((x+side*stretch, y+d+side+d)) # bottom right
    oct.append((x, y+d+side+d)) # bottom left
    oct.append((x-d, y+d+side)) # left bottom
    oct.append((x-d, y+d)) # left top
    oct.append((x, y)) # top left
    return oct

def deform(shp, iterations, variance):
    """
    Take a shape (as a list of vertices) and deform each edge by 2 x variance (-ve, +ve) amount.
    Iterate 'iterations' times.
    Algorithm from https://www.youtube.com/watch?v=5bBkBVnrg2g
    and https://tylerxhobbs.com/essays/2017/a-generative-approach-to-simulating-watercolor-paints
    """
    for i in range(iterations):
        for j in range(len(shp)-1, 0, -1):
            midpoint = ((shp[j-1][0] + shp[j][0])/2 + uniform(-variance, variance), (shp[j-1][1] + shp[j][1])/2 + uniform(-variance, variance))
            shp.insert(j, midpoint)
    return shp

def draw_shape(shp, r, g, b, a):
    """
    Take a list of vertices (shp) and draw the given shape using the
    supplied (r, g, b, a) colour values.
    """
    # stroke(r, g, b, a)
    # strokeWeight(2)
    noStroke()
    fill(r, g, b, a)
    beginShape()
    for v in shp:
        vertex(*v)
    endShape()

def planet_size(s):
    """
    Take a given size amount for a planet and multiply it by the random factor
    chosen from the list using random.choice(). Weight towards medium sized planets.
    
    Should change this to a proper normal distribution at some point.
    """
    sf = [0.3, 0.4, 0.6, 0.6, 0.8, 0.8, 0.9, 1.0, 1.0, 1.1, 1.2, 1.2, 1.5, 1.5, 1.8, 3.0]
    sc = choice(sf)
    return s * sc

def planet(planet_size, distance, ring_colour=(255, 255, 255), planet_colour=(255, 0, 0), rpos=False):
    """
    Draw a planet orbit, shadow, and planet (in that order) using the supplied ring and planet
    colours. Optional 'rpos' randomly positions the planet on its elliptical orbit.
    """
    # orbit ring
    stroke(*ring_colour)
    strokeWeight(4)
    noFill()

    ellipse(750, 1000, distance*1.5, distance)
    
    px = 750
    py = 1000 - distance / 2
    w = distance * 1.5
    h = distance
    if rpos:
        # choose a random x, y position on the orbit
        # choose a random x position for the planet, avoiding the extreme edges
        px = int(random(max([px - w/2, 100]), min([px + w/2, 1400])))
        # calculate the y position based off the ellipse of its orbit
        py = pointOnEllipse(750, 1000, w, h, px)
        
    noStroke()
    # planet shadow
    fill(50, 50, 50, 75)
    circle(px, py, planet_size + 10)
    
    # planet
    noStroke()
    fill(*planet_colour)
    circle(px, py, planet_size) 

def add_noise(thresh=80):
    """
    Create some grainy noise using the supplied threshhold (percentage chance
    of noisy pixel being created).
    """
    ww = color(255, 255, 255, 3)
    bw = color(0, 0, 0, 3)
    strokeWeight(2)
    # noSmooth() # annoying this applies to every step of the process, not just the noise
    # Ideally it'd use the pixels array from processing to achieve this but I couldn't figure
    # out how to turn the integer the array at the specified index gave me into an RGB value
    # to darken/lighten it.
    for x in range(1500):
        for y in range(1000):
            if random(0, 100) >= 80: # reduce total amount of noise
                if random(0, 100) >= 50: # type of noise
                    fill(ww)
                    stroke(ww)
                else:
                    fill(bw)
                    stroke(bw)
                point(x, y)

def draw_nebula(nebs=15, layers=20):
    """
    Use the polygon deformation function to draw some clouds in the background, then use the
    same process to draw darker 'holes' and lighter patches over the top to make it look less
    solid.
    """
    octs = []
    holes = []
    spots = []
    for i in range(nebs):
        s = random(100, 200)
        x = random(0, 1500)
        y = random(0, 1000)
        stretch = random(2,4)
        neb_col = (uniform(0, 0.2)*255, uniform(0.2, 0.4)*255, uniform(0.2, 0.7)*255)
        octs.append((octagon(x, y, s, stretch=stretch), neb_col))
        # generate some holes and spots in the nebula
        for j in range(int(random(10,15))): # holes
            # position of hole
            hx = random(x-s/2, x+s*stretch+s/2)
            hy = random(y-s/2, y+s+s/2)
            # size of hole
            hs = random(s/10, s/3)
            hstr = random(1,4)
            holes.append((octagon(hx, hy, hs, stretch=hstr), (50, 50, 50, uniform(0.5, 2)*255)))
        for j in range(int(random(3,7))): # spots
            hx = random(x-s/2, x+s*stretch+s/2)
            hy = random(y-s/2, y+s+s/2)
            hs = random(s/20, s/10)
            hstr = random(1,4)
            spots.append((octagon(hx, hy, hs, stretch=hstr), (100, 100, 100, uniform(0.05, 0.1)*255)))

    # draw the original clouds
    for j in range(layers):
        for o, c in octs:
            d = deform(o[:], 8, int(random(20,25)))
            draw_shape(d, c[0], c[1], c[2], uniform(0.01,0.02)*255)
    # draw light-ish spots over the clouds
    for j in range(layers):
        for h, c in spots:
            d = deform(h[:], 6, int(random(20,25)))
            draw_shape(d, c[0], c[1], c[2], uniform(0.01,0.02)*255)
    # draw black-ish holes over the clouds
    for j in range(layers):
        for h, c in holes:
            d = deform(h[:], 7, int(random(20,25)))
            draw_shape(d, c[0], c[1], c[2], uniform(0.01,0.02)*255)
    

def setup():
    size(1500, 1000)
    background(*bg)
    frameRate(5)
    
    gc = lambda: (uniform(0.5, 0.9)*255, uniform(0.5, 0.9)*255, uniform(0.5, 0.9)*255) #random colours
    
    # gas clouds
    draw_nebula()
    
    # add grain to space
    add_noise(thresh=80)
    
    planets = randint(5,8)
    avg_dist = 1500.0 / planets
    pos = 0
    for i in range(randint(5,8)):
        ps = planet_size(random(50,150))
        orbit = 1900 - avg_dist * pos + randint(-50, 50)
        pos += 1
        
        planet(ps, orbit, planet_colour=gc(), rpos=True)
    
    add_noise(thresh=80)
    
    #sun and border
    sun_colour=gc()
    planet(300, 0, planet_colour=sun_colour)
    
    # border
    stroke(*sun_colour)
    strokeWeight(50)
    noFill()
    rect(0, 0, 1500, 1000)
    
    print("Done.")

    

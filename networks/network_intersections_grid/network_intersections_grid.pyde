from random import choice

w, h, = 800, 800
points = {}
lines = []

num_points = 10 + int(random(50))
max_conns = 1 + int(random(5))

pointsize = 30.0
lineweight = 3.0

# draw potential lines of intersection
drawIntersect = True
# draw nodes
drawPoints = True
DEBUG = False

# colours
bg_colour = (203, .27, .77)

def intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    # check if any of the points are the same end point
    if ((x1, y1) == (x3, y3) or (x1, y1) == (x4, y4) or (x2, y2) == (x3, y3) or (x2, y2) == (x4, y4)):
        return False
    x12 = x1 - x2
    x34 = x3 - x4
    y12 = y1 - y2
    y34 = y3 - y4
    c = x12 * y34 - y12 * x34
    a = x1 * y2 - y1 * x2
    b = x3 * y4 - y3 * x4
    if c != 0:
        xi = (a * x34 - b * x12) / c
        yi = (a * y34 - b * y12) / c
        # check if these are outside the bounds of the line, since this projects
        # past the potential line ends
        if xi < min((x1, x2)) or xi > max((x1, x2)) or yi < min((y1, y2)) or yi > max((y1, y2)):
            return False
        if xi < min((x3, x4)) or xi > max((x3, x4)) or yi < min((y3, y4)) or yi > max((y3, y4)):
            return False
        if drawIntersect:
            pushMatrix()
            noStroke()
            fill(0, 1, 1)
            circle(xi, yi, 5)
            stroke(0, 0, 0, 0.1)
            line(x1, y1, x2, y2)
            line(x3, y3, x4, y4)
            popMatrix()
        return True
    else:
        return False

def setup():
    global num_points
    size(w, h)
    colorMode(HSB, 360, 1, 1, 1)
    background(*bg_colour)
    
    s = int(random(1000))
    print(s)
    randomSeed(s)
    
    cells = 10
    cellsize = width / cells
    gridx = [x * cellsize + cellsize/2 for x in range(cells)]
    gridy = [y * cellsize + cellsize/2 for y in range(cells)]
    
    while num_points:
        x, y = choice(gridx), choice(gridy)
        if (x, y) not in points:
            points[(x, y)] = 0
            num_points -= 1
    
    noLoop()

def draw():
    
    # draw connections, filtering out intersections
    for px, py in points:
        conns = int(random(max_conns)) + 1
        avail = [p for p in points if p != (px, py)]
        while conns and avail:
            # pick a point
            i = int(random(len(avail)))
            # if a line to that point crosses any other line, filter out that point
            crossed = False
            for l in lines:
                if l == (avail[i][0], avail[i][1], px, py): # same line but backwards
                    del avail[i]
                    crossed = True
                    break
                if intersect(px, py, avail[i][0], avail[i][1], l[0], l[1], l[2], l[3]):
                    del avail[i]
                    crossed = True
                    break
            if not crossed:
                conns -= 1
                lines.append((px, py, avail[i][0], avail[i][1]))
                points[(px, py)] += 1
                points[(avail[i][0], avail[i][1])] += 1
                if DEBUG:
                    pushMatrix()
                    strokeWeight(0.5)
                    stroke(250, 1, 1)
                    line(px, py, avail[i][0], avail[i][1])
                    popMatrix()
                    
    maxconns = max(points.values())
    stroke(0, 1, 1, 0.8)
    for l in lines:
        strokeWeight(0.5)
        p1, p2 = (l[0], l[1]), (l[2], l[3])
        lineperc = (points[p1] + points[p2]) / 2 / maxconns
        strokeWeight(0.5 + lineweight * lineperc)
        line(l[0], l[1], l[2], l[3])
    if drawPoints:
        for x, y in points:
            pushMatrix()
            noStroke()
            sizeperc = points[(x, y)] / float(maxconns)
            fillcolour = 100 - (100.0 * sizeperc)
            fill(fillcolour, 1, 1)
            circle(x, y, 5 + sizeperc * pointsize)
            popMatrix()

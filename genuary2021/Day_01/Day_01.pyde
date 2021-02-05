# Genuary Day 1
from random import shuffle, choice
coords = []
cellsize = 50
sat = 0.54
bright = 0.97
colours = [0, 53, 79, 123, 188, 205, 237, 271]

def setup():
    size(800, 800)
    colorMode(HSB, 360, 1, 1, 1)
    noStroke()
    noLoop()

def draw():
    cells = int(width/cellsize)
    xcells = [x for x in range(cells)]
    ycells = [y for y in range(cells)]
    shuffle(xcells)
    shuffle(ycells)
    for b in [BLEND, MULTIPLY, DIFFERENCE]:
        blendMode(b)
        for x in xcells:
            for y in ycells:
                c = choice(colours)
                fill(c, sat, bright)
                xc, yc = x * cellsize + cellsize/2.0, y * cellsize + cellsize/2.0
                sides = choice([0, 3, 4, 5])
                r = random(cellsize/2.0, cellsize*1.2)
                if sides == 0:
                    circle(xc, yc, r)
                else:
                    a = random(TWO_PI)
                    beginShape()
                    for i in range(sides):
                        vertex(cos(i*TWO_PI/sides+a)*r+xc, sin(i*TWO_PI/sides+a)*r+yc)
                    endShape(CLOSE)
    saveFrame("day1.png")

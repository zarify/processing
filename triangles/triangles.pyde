# triangle decay
# could either have a lower chance of making triangles
# or make the colours in the triangles dimmer as they get further away
# or both?

# develop this into a celular automaton
# neighbour cells could have rules as to what colour triangle is in it
# maybe some random colour generation as well

# TODO: run multiple generations and animate

from random import seed, randint
w, h = 1000, 1000
rx, ry = 0, 0
incircles = True

cell_size = 50
# incircle calcs for top-left corner triangle - offsets only
hyp = sqrt(cell_size**2 + cell_size**2)
in_x = (cell_size**2)/(cell_size*2 + hyp)
in_y = (cell_size**2)/(cell_size*2 + hyp)


# keep track of the state of each cell
# filled: 0/1, colour: (r,g,b,a), inverted: 0/1
cells = [[{'filled': 0, 'colour': [0, 0, 0], 'inverted': 0, 'alpha': 255} for x in range(int(w/cell_size))] for y in range(int(h/cell_size))]

# rules
#   colour of neighbours influence colour of shape
#   number of neighbours influence whether it is darker or lighter
#   inversion status of neighbours influence likelihood to be inverted itself
#   distance from epicenter influences alpha value

def tri(x, y, colour, invert=0, a=100):
    """
    Draw a triangle using the given x, y index positions as a base.
    Inversion refers to where in the quadrant specified by the index the triangle
    is drawn.
    """
    x *= cell_size
    y *= cell_size

    noStroke()
    fill(colour[0], colour[1], colour[2], a)
    if invert == 1: # top right
        triangle(x, y, x + cell_size, y, x + cell_size, y + cell_size)
        cx, cy = cell_size + x - in_x, y + in_y
    elif invert == 2: # bottom right
        triangle(x + cell_size, y, x + cell_size, y + cell_size, x, y + cell_size)
        cx, cy = cell_size + x - in_x, cell_size + y - in_y
    elif invert == 3: # bottom left
        triangle(x, y, x + cell_size, y + cell_size, x, y + cell_size)
        cx, cy = x + in_x, cell_size + y - in_y
    else: # top left
        triangle(x, y, x + cell_size, y, x, y + cell_size)
        cx, cy = x + in_x, y + in_y
    
    # randomly draw a circle inside some triangles?
    # calculate x/y distance from corner
    # maybe randomly draw the incircle in the space not filled by the triangle
    
    if randint(0, 100) > 97 and incircles:
        fill(random(360), 50, 90, 100)
        circle(cx, cy, int(in_x*2))

def cell(x, y):
    """
    Process the cell at the x/y indices (not coordinates) according to the current
    grid state for the automata rules.
    """
    try:
        if cells[y][x]['filled'] == 1:
            return # this has already been processed
    except IndexError:
        return
    cells[y][x]['filled'] = 1 # this cell is now filled

    nn = []
    for nx, ny in neighbours(x, y):
        try:
            if cells[ny][nx]['filled']:
                nn.append(cells[ny][nx])
        except IndexError:
            continue
    
    c = 0 # colour weighting
    
    #------ Flippedness
    flipped = sum([i['inverted'] for i in nn if i['inverted']])
    cells[y][x]['inverted'] = (randint(0, 3) + flipped) % 4
    
    #------- Colour calculation
    avg_colour = sum([i['colour'][0] for i in nn]) / len(nn)
    avg_sat = sum([i['colour'][1] for i in nn]) / len(nn)
    avg_bri = sum([i['colour'][2] for i in nn]) / len(nn)
    
    # small chance of going totally random otherwise small variation from neighbours
    if random(100) > 90:
        h = randint(0, 100)
        s = randint(0, 100)
        b = randint(0, 100)
    else:
        h = (avg_colour + randint(-15, 15)) % 100
        s = (avg_sat + randint(-15, 15)) % 100
        b = (avg_bri + randint(-15, 15)) % 100
    cells[y][x]['colour'] = (h, s, b)
    
    #------- Alpha calculation
    d = sqrt((x*cell_size - rx)**2 + (y*cell_size - ry)**2) # distance from epicenter
    mx = sqrt((w-rx*cell_size)**2 + (h-ry*cell_size)**2)
    a = d/sqrt(w**2+h**2)*255
    cells[y][x]['alpha'] = a
    
    for cx,cy in neighbours(x, y):
        cell(cx, cy)
    

def neighbours(x, y):
    """
    Find the coordinates of the neighbours of the given cell and return them in a flat list.
    """
    n = []
    for c in ((y-1, x-1), (y-1, x), (y-1, x+1), (y, x-1), (y, x+1), (y+1, x-1), (y+1, x), (y+1, x+1)):
        n.append(c)
    return n

def background_crosshatch(passes=1, randomness=0, steps=4):
    # cross hatch background for a bit of texture
    stroke(0, 0, 0, 20)
    strokeWeight(1)
    for i in range(0, w, steps):
        # if random_background is set, choose a random start and endpoint for each line
        if random_background:
            xoff = random(i)
            yoff = random(i-xoff)
            
            tr_x = i - xoff
            tr_y = tan(radians(45.0)) * xoff
            
            bl_x = tan(radians(45.0)) * yoff
            bl_y = i - yoff
            
            line(tr_x, tr_y, bl_x, bl_y)
            
            # other half of the square now!
            off = random(i)
            yoff = random(i-xoff)
            
            tr_x = i - xoff
            tr_y = tan(radians(45.0)) * xoff
            
            bl_x = tan(radians(45.0)) * yoff
            bl_y = i - yoff
            
            line(w-tr_x, h-tr_y, w-bl_x, h-bl_y)

        else:
            line(i, 0, 0, i)
            line(i, h, w, i)
    if passes == 2:
        for i in range(0, h, steps):
        # if random_background is set, choose a random start and endpoint for each line
        if random_background:
            xoff = random(i)
            yoff = random(i-xoff)
            
            tr_x = i - xoff
            tr_y = tan(radians(45.0)) * xoff
            
            bl_x = tan(radians(45.0)) * yoff
            bl_y = i - yoff
            
            line(tr_x, tr_y, bl_x, bl_y)
            
            # other half of the square now!
            off = random(i)
            yoff = random(i-xoff)
            
            tr_x = i - xoff
            tr_y = tan(radians(45.0)) * xoff
            
            bl_x = tan(radians(45.0)) * yoff
            bl_y = i - yoff
            
            line(w-tr_x, h-tr_y, w-bl_x, h-bl_y)

        else:
            line(i, 0, 0, i)
            line(i, h, w, i)

def setup():
    global rx, ry
    size(w, h)
    colorMode(HSB, 100)
    
    # randomSeed(42)
    # seed(42)
    
    background(0, 0, 100)
    background(randint(0, 100), randint(20, 30), randint(60, 90), random(20, 50))
    
    background_crosshatch(passes=1, randomness=1)
    
    # starting position
    rx, ry = randint(0, len(cells[0])-1), randint(0, len(cells)-1) 
    print(rx, ry)
    
    m = sqrt((w-rx)**2 + (h-ry)**2)
    
    # initial cell values
    cells[ry][rx]['filled'] = 1
    cells[ry][rx]['inverted'] = randint(0, 3)
    cells[ry][rx]['colour'] = (randint(0,100), randint(50,100), randint(50, 100), 100) # HSB
    
    print(cells[ry][rx]['colour'])
    
    # now recursively process all other cells by analysing nearest neighbours
    cn = neighbours(rx, ry)
    for x,y in cn:
        cell(x, y)
    
    # finally, draw the triangles for every cell
    for y in range(len(cells)):
        for x, c in enumerate(cells[y]):
            pass
            tri(x, y, c['colour'], c['inverted'], c['alpha'])
    
    save("tri10.png")
    

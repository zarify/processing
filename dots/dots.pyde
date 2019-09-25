from random import uniform, randint, choice

# placement data

grid_size = 12 # smallest size possible
cell_size = 8 # w, h of cell in grid size multiples
circles = [] # (x, y, r)

# general config

c_w = 10 * grid_size * cell_size
c_h = 10 * grid_size * cell_size
c = (random(100, 900), random(100, 900))
space = grid_size / 4
r = grid_size * 3 / 4
max_shadow = (r/2 + space*1.25) # max possible distance shadow can be from parent

# fill canvas with dots
rows = int(c_w / (r + space))
cols = int(c_h / (r + space))

def calc_offset(from_p, to_p):
    """
    Calculate the x, y shadow offset as a percentage, based on the dot's distance
    from the 'low' point. This is relative to the total width/height of the canvas.
    """
    x, y = from_p
    tx, ty = to_p
    dx = (tx - x) / c_w
    dy = (ty - y) / c_h
    return (dx, dy)

def shadow_circle(x, y, r, bw=True):
    """
    Draw a series of cocentric transparent shadow circles to get the blur effect.
    Could probably be better achieved by using a blur filter on the right
    type of processing object.
    bw parameter controls whether shadows are drawn in dark grey (True) or
    a soft colour (False).
    """
    # get a nice random colour if not using black and white
    noStroke()
    if not bw:
        s_col = (uniform(0.3, 0.7)*255, uniform(0.3, 0.7)*255, uniform(0.3, 0.7)*255, 15)
    else:
        s_col = (50, 50, 50, 15)
    for i in range(int(r),0,-1):
        fill(*s_col)
        circle(x, y, i)

def gen_circles(max_size=0, max_circles=0, max_area=0):
    """
    Generate a grid of circles by packing groups of cells with random sizes.
    Uses a square grid, which means there is some dead space around the largest
    circles.
    Parameters are:
        max_size - maximum circle size (in cell grid increments) to be generated
        max_circles - maximum number of circles to be contained in a single cell
        max_area - maximum circle area (in cell grid increments) in a single cell
    Passing nothing (or 0) for any parameter will set them to the maximum possible
    amount for all generated cells.
    Passing -1 for any parameter will set them to a random amount on a cell-by-cell
    basis.
    """
    # uniform generation rules
    if max_size == 0:
        max_size = cell_size
    if max_circles == 0:
        max_circles = cell_size * cell_size
    if max_area == 0:
        max_area = cell_size * cell_size
    
    # iterate through cell boxes for population
    for r_y in range(c_w / (grid_size * cell_size)):
        for r_x in range(c_w / (grid_size * cell_size)):
            current_circles = 0
            current_area = 0
            cell_circles = [['.']*cell_size for j in range(cell_size)]
            # per cell random generation rules
            if max_size == -1:
                c_max_size = randint(1, cell_size)
            else:
                c_max_size = max_size
            if max_circles == -1:
                c_max_circles = randint(1, cell_size * cell_size)
            else:
                c_max_circles = max_circles
            if max_area == -1:
                c_max_area = randint(1, cell_size * cell_size)
            else:
                c_max_area = max_area

            # go through the cell and pack it with circles until there is
            # no more space, working in multiples of grid_size
            while True:
                biggest = 0
                free = False
                possibles = [] # possible positions for biggest circle
                # work through each coordinate in the current cell
                for x in range(cell_size):
                    for y in range(cell_size):
                        # don't bother checking if this cell is currently occupied
                        if cell_circles[y][x] == '#':
                            continue
                        cur_biggest = 1 # biggest possible circle radius seen so far
                        offset = 0 # how far we've looked away from x, y
                        while True:
                            if (x + offset) >= cell_size or (y + offset) >= cell_size: # out of bounds
                                break
                            if cell_circles[y+offset][x+offset] == '#' or cell_circles[y+offset][x] == '#' or cell_circles[y][x+offset] == '#': # hit a circle
                                break
                            cur_biggest += 1 # grow current circle
                            offset += 1
                            free = True
                            if cur_biggest == c_max_size:
                                break
                            if (current_area + cur_biggest * cur_biggest) >= c_max_area:
                                break
                        if cur_biggest > biggest: # new biggest encountered, reset coords
                            possibles = [(x, y)]
                            biggest = cur_biggest
                            offset = 0
                        elif cur_biggest == biggest: # equal biggest, add to coords
                            possibles.append([x, y])        
                if not free or current_circles >= c_max_circles or current_area >= c_max_area: # no space found or too many circles
                    break
                else:
                    # create a circle of random(1,biggest) size and then place
                    # in one of the possible locations
                    # then fill out the cell_circles list to modify the free space array
                    circle_size = randint(1, biggest-1)
                    circle_pos = choice(possibles)

                    fx = circle_pos[0] * grid_size + grid_size * r_x * cell_size + grid_size / 2
                    fy = circle_pos[1] * grid_size + grid_size * r_y * cell_size + grid_size / 2
                    
                    fx += circle_size * r / 2
                    fy += circle_size * r / 2
                    
                    # space calculation around each object
                    fx += circle_size * space / 2
                    fy += circle_size * space / 2
                    
                    circles.append((fx, fy, circle_size * r))
                    for y_off in range(circle_size):
                        for x_off in range(circle_size):
                            cell_circles[circle_pos[1]+y_off][circle_pos[0]+x_off] = '#'
                    current_circles += 1
                    current_area += circle_size * circle_size
        

def setup():
    size(c_w, c_h)
    background(255, 255, 255)

    
    gen_circles(max_size=5, max_circles=-1, max_area=-1)
    print("num circles",len(circles))
    # shadows
    for x, y, r in circles:
        # offset refers to shadow's distance and direction from parent
        # based on where the bright 'center' point of the image is
        dx, dy = calc_offset((x, y), c)
        shadow_circle(x + max_shadow * dx, y + max_shadow * dy, r, bw=True)
    # objects
    for x, y, r in circles:
        noStroke()
        fill(255, 255, 255)
        circle(x, y, r)
    print("Done.")
    save("dots.png")


    

    

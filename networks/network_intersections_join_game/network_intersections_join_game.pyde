# Could also gamify this basic idea by having nodes not connected and having to connect them all without crossing lines
# this would require checking to make sure games were solvable however. - only if perfect game
# one solution could be to work outwards from a random node each time for placement, placing connectors the first time
# to ensure valid moves

# put in a time limit - DONE
# add in an sqlite database, record the seed used to generate the level, maybe have a level selector - NO SQLITE >:(

import time

w, h, = 800, 800
points = {} # id: NetworkNode
connectors = {} # id: Connector

num_points = 10 + int(random(50))
max_conns = 5
sticky_distance = 150
speed = 0.5
lastClicked = -1

pointsize = 30.0
lineweight = 5.0
node_size = 10
cells = 10
max_time = 90
time_left = max_time

bg_colour = (203, .27, .77)
bg_timeout = (0, .38, .8)
level_seed = 0

game_over = False
start_time = time.time()

class NetworkNode:
    def __init__(self, x, y, conns, sticky, id):
        self.x, self.y = x, y
        self.max_conns = conns # maximum number of connections
        self.sticky = sticky # distance to break connections
        self.connections = [] # list of connected connections
        self.id = id # numerical ID for global id purposes
        self.stroke_colour = (0, 0, 0)
        self.node_size = 5 + 20 * (sticky / (2 * sticky_distance))
        self.selected = False
    
    def add_connection(self, connector):
        self.connections.append(connector)
    
    def break_connection(self, connector):
        # I don't _think_ this error happens anymore
        try:
            self.connections.remove(connector)
        except:
            print("Tried to remove {} but failed".format(connector))
    
    def conns(self):
        return len(self.connections)
    
    def draw_me(self):
        pushStyle()
        if self.selected:
            stroke(0, 0, 1)
            noFill()
            strokeWeight(0.5)
            circle(self.x, self.y, self.sticky)
            strokeWeight(3)
        else:
            strokeWeight(1)
        stroke(0)
        if self.max_conns > self.conns():
            fill(30, .88, .84)
        else:
            fill(155, .88, .84)
        circle(self.x, self.y, self.node_size)
        fill(0)
        textAlign(CENTER, CENTER)
        text(str(self.max_conns-len(self.connections)), self.x, self.y)
        popStyle()
    
    def was_clicked(self, mx, my):
        return PVector(mx, my).dist(PVector(self.x, self.y)) <= self.node_size/2
    
    def click(self):
        self.selected = not self.selected
    
    def can_connect(self, node):
        d = PVector(self.x, self.y).dist(PVector(node.x, node.y))
        return self.conns() < self.max_conns and node.conns() < node.max_conns and d < self.sticky/2 and node not in self.connections
    
    def __str__(self):
        return "[{}, {}], {} of {}, {}".format(int(self.x), int(self.y), self.conns(), self.max_conns, int(self.sticky))

class Connector:
    def __init__(self, nodes):
        self.endpoints = nodes
        self.id = "_".join(map(str,sorted([nodes[0].id, nodes[1].id])))
    
    def draw_me(self):
        end1 = [self.endpoints[0].x, self.endpoints[0].y]
        end2 = [self.endpoints[1].x, self.endpoints[1].y]
        # average the stickiness of the two ends, and use the length to get how 'stretched' the line is
        # as a percentage
        p = 1.0 - self.get_length() / ((self.endpoints[0].sticky + self.endpoints[1].sticky)/2.0)
        pushStyle()
        stroke(0, 1, 1-p)
        strokeWeight(lineweight * p)
        line(*(end1+end2))
        popStyle()
    
    def get_ends(self):
        return [self.endpoints[0].x, self.endpoints[0].y, self.endpoints[1].x, self.endpoints[1].y]

    def get_length(self):
        return PVector(self.endpoints[0].x, self.endpoints[0].y).dist(PVector(self.endpoints[1].x, self.endpoints[1].y))
    
    def disconnect(self):
        self.endpoints[0].break_connection(self)
        self.endpoints[1].break_connection(self)
    
    def check_for_break(self):
        return self.get_length() > min((self.endpoints[0].sticky, self.endpoints[1].sticky))
    
    def __str__(self):
        return "{}:\n\t{}\n\t{}".format(self.id, self.endpoints[0], self.endpoints[1])
    
def intersect(x1, y1, x2, y2, x3, y3, x4, y4, drawIntersect=False):
    # algorithm I found on some random site because laziness with some tweaks as it also
    # counted intersections on projections of either line, not just between the end points
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
            pushStyle()
            noStroke()
            fill(0, 1, 1)
            circle(xi, yi, 5)
            # stroke(0, 0, 1, 0.1)
            # line(x1, y1, x2, y2)
            # line(x3, y3, x4, y4)
            popStyle()
        return True
    else:
        return False

def get_score():
    return (sum([len(points[i].connections) for i in points]), sum([points[i].max_conns for i in points]))

def setup_board():
    global num_points, level_seed
    level_seed = int(random(10000))
    randomSeed(level_seed)
    
    # populate points
    xcellsize = width/cells
    ycellsize = height/cells
    print(cells, xcellsize, ycellsize)
    coords = []
    for x in range(cells):
        for y in range(1,cells-1):
            coords.append((x * xcellsize + xcellsize/2, y * ycellsize + ycellsize/2))
    i = 0
    np = num_points
    while num_points and coords:
        x, y = coords.pop(int(random(len(coords))))
        points[i] = NetworkNode(x, y, int(random(max_conns))+1, sticky_distance + random(sticky_distance), i)
        num_points -= 1
        i += 1

def setup():
    size(w, h)
    colorMode(HSB, 360, 1, 1, 1)
    background(*bg_colour)
    frameRate(30)
    #noLoop()
    
    setup_board()

def draw():
    global time_left, game_over, lastClicked
    
    if game_over:
        background(*bg_timeout)
    else:
        background(*bg_colour)
    
    # check for link breakages or whether the lines intersect a current line after movement
    breaks = set()
    for i in connectors:
        if connectors[i].check_for_break():
            breaks.add(i)
        for j in connectors:
            if i == j:
                continue
            if intersect(*(connectors[i].get_ends() + connectors[j].get_ends())):
                breaks.add(i)
                breaks.add(j)
    for i in sorted(breaks, reverse=True):
        connectors[i].disconnect()
        del connectors[i]
    
    # connect nodes, avoiding intersections
    lines = [connectors[c].get_ends() for c in connectors] # populate with current set of lines first
    
    # draw connection lines between any clicked points and the mouse cursor, highlighting intersections
    for p in [i for i in points if points[i].selected]:
        pushStyle()
        stroke(0, 0, 1)
        strokeWeight(0.5)
        # limit this line to the stickiness of the point
        d = PVector(mouseX - points[p].x, mouseY - points[p].y).mag()
        if d <= points[p].sticky/2:
            mx, my = mouseX, mouseY
        else:
            hv = PVector(mouseX - points[p].x, mouseY - points[p].y).heading()
            mx = cos(hv) * points[p].sticky/2 + points[p].x
            my = sin(hv) * points[p].sticky/2 + points[p].y
        line(points[p].x, points[p].y, mx, my)
        popStyle()
        for c in connectors:
            ends = connectors[c].get_ends() + [mx, my, points[p].x, points[p].y]
            intersect(*ends, drawIntersect=True)
    
    # draw lines and nodes
    for i in connectors:
        connectors[i].draw_me()
        #print(connectors[i])
    for i in points:
        points[i].draw_me()
    
    # Draw the current score (connections of max connections)
    pushStyle()
    fill(0)
    textSize(20)
    text(" of ".join(map(str, get_score())), 10, 20)
    textAlign(CENTER)
    text("Seed {}".format(level_seed), width/2, 20)
    
    if not game_over:
        time_left = max_time-(time.time()-start_time)
        if time_left < 0.01:
            game_over = True
            time_left = 0
            # deselect any clicked nodes
            for i in points:
                points[i].selected = False
            lastClicked = -1

    if game_over:
        fill(0, .96, .46)
    textAlign(RIGHT)
    text("{:.1f} seconds".format(time_left), width-10, 20)
    popStyle()
    

def mouseClicked():
    # there's a clicking bug that looks like it's in Processing's event handling
    # means some clicks aren't caught properly
    global lastClicked
    if game_over:
        return
    
    clicks = [i for i in points if points[i].was_clicked(mouseX, mouseY)]
    #print(lastClicked, clicks, connectors.keys()) # DEBUG
    if lastClicked == -1 or (clicks and lastClicked == clicks[0]):
        # clicking a selected node or no node selected
        if clicks:
            points[clicks[0]].click()
            lastClicked = clicks[0] if lastClicked == -1 else -1
        # otherwise we've clicked on space, not a node
    elif clicks:
        # check if these nodes are already connected and break if so
        cid = "_".join(map(str,sorted((lastClicked, clicks[0]))))
        #print("\t{}".format(cid)) # DEBUG
        if cid in connectors:
            connectors[cid].disconnect()
            del connectors[cid]
            points[lastClicked].selected = False
            points[clicks[0]].selected = False
            lastClicked = -1
        # check if these two nodes can be connected
        elif points[lastClicked].can_connect(points[clicks[0]]):
            c = Connector((points[lastClicked], points[clicks[0]]))
            # break any intersecting connections
            breaks = set()
            ends = c.get_ends()
            for i in connectors:
                l_ends = connectors[i].get_ends()
                if intersect(*(l_ends + ends)):
                    breaks.add(i)
            for i in sorted(breaks, reverse=True):
                connectors[i].disconnect()
                del connectors[i]
            connectors[c.id] = c
            points[lastClicked].add_connection(c)
            points[clicks[0]].add_connection(c)
                
            points[lastClicked].click()
            lastClicked = -1
        else: # ???
            # not connected, and not valid for a connection to the last clicked node
            # maybe play a little animation?
            pass

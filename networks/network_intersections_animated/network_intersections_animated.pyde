# I really want to add in elasticity to the connections so they actually pull the nodes around
# TODO: Put a cooldown on re-attaching after snapping

w, h, = 800, 800
points = {} # id: NetworkNode
connectors = {} # id: Connector

num_points = 10 + int(random(50))
max_conns = 5
sticky_distance = 150
speed = 0.5
cooldown = 10 # how many frames to keep a connection broken before trying it again

pointsize = 30.0
lineweight = 5.0
node_size = 10

# draw dots showing intersection points
drawIntersect = True
# draw lines which were discarded due to intersections
drawFailedLines = True

bg_colour = (203, .27, .77)

class NetworkNode:
    def __init__(self, x, y, conns, sticky, id):
        self.x, self.y = x, y
        self.xvec, self.yvec = random(-speed, speed), random(-speed, speed)
        self.max_conns = conns # maximum number of connections
        self.sticky = sticky # distance to break connections
        self.connections = [] # list of connected connections
        self.id = id # numerical ID for global id purposes
        self.stroke_colour = (0, 0, 0)
        self.node_size = 5 + 20 * (sticky / (2 * sticky_distance))
        self.cooldown = 0
    
    def add_connection(self, connector):
        self.connections.append(connector)
    
    def break_connection(self, connector):
        self.connections.remove(connector)
        self.cooldown = cooldown
    
    def conns(self):
        return len(self.connections)
    
    def draw_me(self):
        pushStyle()
        strokeWeight(1)
        stroke(0)
        if self.max_conns > self.conns():
            fill(30, .88, .84)
        else:
            fill(155, .88, .84)
        circle(self.x, self.y, self.node_size)
        popStyle()
        self.cooldown = self.cooldown - 1 if self.cooldown else 0
    
    def move(self):
        "Shuffle this point slightly, bouncing at edges"
        self.x += self.xvec
        self.y += self.yvec
        if self.x <= self.node_size or self.x >= (width-self.node_size):
            self.xvec *= -1
        if self.y <= self.node_size or self.y >= (height-self.node_size):
            self.yvec *= -1
    
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
    
def intersect(x1, y1, x2, y2, x3, y3, x4, y4):
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
            if drawFailedLines:
                stroke(0, 0, 1, 0.1)
                line(x1, y1, x2, y2)
                line(x3, y3, x4, y4)
            popStyle()
        return True
    else:
        return False

def setup():
    size(w, h)
    colorMode(HSB, 360, 1, 1, 1)
    background(*bg_colour)
    
    s = int(random(10000))
    print("Seed: {}".format(s))
    randomSeed(s)
    #randomSeed(42)
    
    # populate points
    for i in range(num_points):
        x, y = random(w-w/10.0)+w/15, random(h-h/10.0)+h/15
        # current connections, maximum connections, distance to break, global node id
        points[i] = NetworkNode(x, y, int(random(max_conns))+1, sticky_distance + random(sticky_distance), i)

    frameRate(30)
    #noLoop()

def draw():
    background(*bg_colour)
    
    for i in points:
        points[i].move()
    
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
    for i in points:
        px, py = points[i].x, points[i].y
        avail = [j for j in points if points[j].conns() < points[j].max_conns and j != i and points[j].cooldown == 0]
        while points[i].conns() < points[i].max_conns and avail:
            j = int(random(len(avail)))
            ax, ay = points[avail[j]].x, points[avail[j]].y
            # determine if:
            #    a) this line would exceed the sticky distance of either end point; or
            #    b) this connection crosses a current line
            point_dist = PVector(px, py).dist(PVector(ax, ay))
            if point_dist > points[i].sticky/2 or point_dist > points[avail[j]].sticky/2:
                del avail[j]
                continue
            if points[avail[j]].conns() >= points[avail[j]].max_conns:
                del avail[j]
                continue
            
            crossed = False
            for l in lines:
                if l == (ax, ay, px, py): # same line reversed
                    del avail[j]
                    crossed = True
                    break
                if intersect(px, py, ax, ay, l[0], l[1], l[2], l[3]):
                    del avail[j]
                    crossed = True
                    break
            if not crossed:
                #print("Added connector from {} to {}".format(i,avail[j]))
                c = Connector((points[i], points[avail[j]]))
                if c.id in connectors:
                    del avail[j]
                    continue
                connectors[c.id] = c
                points[i].add_connection(c)
                points[avail[j]].add_connection(c)
                lines.append((px, py, ax, ay))
    
    # draw lines and nodes
    for i in connectors:
        connectors[i].draw_me()
        #print(connectors[i])
    for i in points:
        points[i].draw_me()
    #print("Connections: {}".format(len(connectors)))

add_library('serial')
# something other than a computer as a source of randomness

from random import choice

#--------------------------------- Serial boilerplate
ser = Serial(this, "COM10", 115200)
serialBuffer = []
buttonBuffer = []
currentReading = {
                  "x": 0, # -1023 to 1023
                  "y": 0,
                  "z": 0,
                  "bright": 0, # 0-1023
                  "sound": 0, # 0-255
                  }

def getSerial():
    global serialBuffer, buttonBuffer
    s = ser.readString()
    if s:
        s = [x for x in s.strip().split() if x != []]
        if len(s):
            serialBuffer += s
        if serialBuffer:
            try:
                b = serialBuffer.pop(0).split(",")
                if b[0] == "button":
                    if b[1] == "A":
                        buttonBuffer.append("A")
                    elif b[1] == "B":
                        buttonBuffer.append("B")
                    elif b[1] == "AB":
                        buttonBuffer.append("AB")
                else:
                    levels = map(int, b)
                    if len(levels) == 5:
                        for label, reading in zip(("x","y","z","bright","sound"), levels):
                            if label == "sound":
                                currentReading[label] = reading / 255.0
                            elif label in ["x", "y", "z"]:
                                currentReading[label] = (reading+1023) / 2046.0
                            else:
                                currentReading[label] = reading / 1024.0 # store as percentage
            except:
                pass # could be no data, malformed input etc

#--------------------------------- MAIN

poly_history = []
polysize = 200
polysides = 30
max_poly = 5 # number of iterations of the polygon to keep
other_shapes = [] # [sx, sy, how many points, colour, rotation, radius, movevector, angle change]

def draw_poly(px, py, sz, snd, col, polysides):
    # sound influences 'spikiness' of the polygon
    current = []
    if len(poly_history) > max_poly:
        poly_history.pop(0)
    for i in range(polysides):
        x, y = cos(i*TWO_PI/polysides) * sz + random(-snd*3,snd*3)*sz/2.0 + px, sin(i*TWO_PI/polysides) * sz + random(-snd*3,snd*3)*sz/2.0 + py
        current.append((x, y))
    poly_history.append([col, current])
    
    pushStyle()
    noStroke()
    for i, (c, p) in enumerate(poly_history):
        c[3] *= (1.0-i/len(poly_history))
        fill(*c)
        beginShape()
        curveVertex(p[0][0], p[0][1])
        for x, y in p:
            curveVertex(x, y)
        curveVertex(x, y)
        endShape(CLOSE)
    popStyle()

def draw_others():
    for sx, sy, points, c, rot, rad, m, a in other_shapes:
        pushStyle()
        fill(*c)
        
        beginShape()
        for i in range(points):
            x = cos(i*TWO_PI/points+rot)*rad+sx
            y = sin(i*TWO_PI/points+rot)*rad+sy
            vertex(x, y)
        endShape(CLOSE)
        popStyle()

def move_others():
    for i, s in enumerate(other_shapes):
        sx, sy, points, c, rot, rad, m, a = s
        dx, dy = m
        
        other_shapes[i][4] = (other_shapes[i][4] + a) % TWO_PI
        if (sx - rad) < 0 or (sx + rad) > width:
            other_shapes[i][6][0] *= -1
        if (sy - rad) < 0 or (sy + rad) > height:
            other_shapes[i][6][1] *= -1
            
        other_shapes[i][0] += other_shapes[i][6][0]
        other_shapes[i][1] += other_shapes[i][6][1]
        
        if frameCount % 30 == 0:
            # add or remove a vertex
            r = random(1)
            if r > 0.5:
                if points > 3:
                    other_shapes[i][2] -= 1
                else:
                    other_shapes[i][2] += 1
            else:
                if points < 10:
                    other_shapes[i][2] += 1
                else:
                    other_shapes[i][2] -= 1

def setup():
    size(800, 800)
    colorMode(HSB, 360, 1, 1, 1)
    
    background(0, 0, 1)
    noStroke()

def draw():
    
    # get data from serial
    getSerial()
    l = currentReading["bright"]
    #background(0, 0, l)
    pushStyle()
    fill(0, 0, 1, l/3)
    square(0, 0, width)
    popStyle()
    # buttons spawn and delete
    if len(buttonBuffer):
        b = buttonBuffer.pop(0)
        if b == u"A":
            p = int(random(4,10))
            sz = random(30, 60)
            other_shapes.append([random(sz,width-sz), # x
                                random(sz, height-sz), # y
                                p, # number of points
                                (random(360), 0.5, 0.5, 0.8), # colour
                                random(TWO_PI), # starting angle
                                sz, # radius
                                [random(-2,2), random(-2,2)], # move vector
                                radians(random(1,5)) # rotation change
                                ])
        elif b == u"B":
            if len(other_shapes):
                i = int(random(len(other_shapes)))
                other_shapes.pop(i)
    
    move_others()
    draw_others()
    # manipulate the visuals based off the serial data
    # sound: polygon spikiness
    # x accel: colour
    # y: size
    c = currentReading["x"] * 360
    b = currentReading["y"]
    draw_poly(400, 400, 100+100*b, currentReading["sound"], [c, 0.6, 0.6, 0.5], polysides)

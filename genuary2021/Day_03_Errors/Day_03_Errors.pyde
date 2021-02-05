err_colour = [0, 0, 0, 1]
text_colour = [0, 0, 0, 1]

x_off = 240
err_off = 110
human_off = 50
err_size = 50

recording = True

class Err:
    def __init__(self):
        global err_size
        self.x = 0
        self.y = 0
        self.rotation = 0
        self.textsize = err_size
        self.colour = [0, 1, 1, 0.5]
        self.mode = REPLACE
        self.delete = False
    
    def glitch(self):
        if frameCount == 50:
            self.colour = [0, 1, 1, 0.5]
        self.x += random(-4,4)
        self.y += random(-4,4)
        self.colour[3] -= 0.002
        self.textsize += random(2)
        self.rotation += random(-HALF_PI/12,HALF_PI/12)
        if self.colour[3] <= 0:
            self.delete = True
    
    def draw_me(self):
        pushMatrix()
        translate(width/2 + self.x, height/2 + self.y)
        fill(*self.colour)
        stroke(0,0,1)
        strokeWeight(1)
        textSize(self.textsize)
        textAlign(CENTER, CENTER)
        rotate(self.rotation)
        text("ERR", 0, 0)
        popMatrix()

errors = []

def glitch():
    global err_colour, text_colour
    if frameCount == 50:
        background(0)
        err_colour = [0, 1, 1, 0.5]
        text_colour = [0, 0, 1, 1]
        blendMode(BLEND)
    elif frameCount < 50:
        background(0, 0, 1)
    if frameCount > 50 and frameCount % 50 == 0:
        e = Err()
        h = random(360)
        e.colour = [h, 1, 1, 0.5]
        errors.append(e)

def setup():
    size(800, 800)
    colorMode(HSB, 360, 1, 1, 1)
    background(0, 0, 1)
    
    frameRate(30)
    #noLoop() # ditch this for progressive glitching later
    e = Err()
    e.colour = [0, 0, 0, 1]
    errors.append(e)

def draw():
    
    glitch() # only redraw the background until glitch time, switch colours
    if frameCount >= 50 and frameCount % 1 == 0:
        for e in errors:
            e.glitch()
    
    pushStyle()
    textSize(50)
    fill(*text_colour)
    textAlign(CENTER, CENTER)
    if frameCount <= 50:
        text("TO", width/2, height*0.2)
        text("IS HUMAN", width/2, height*0.8)
    popStyle()

    for e in errors:
        e.draw_me()
    
    for i in range(len(errors))[::-1]:
        if errors[i].delete:
            del errors[i]
    
    if recording:
        saveFrame("frames/#####.jpg")
        
def mouseClicked():
    saveFrame("Day_03_capture.png")

from string import punctuation
from string import ascii_lowercase as alc
from random import choice, randint, seed

recording = True

#-----------------------MARKOV SECTION------------------------------------
rs = randint(0, 10000)
maxWords = 15

book = "books/angel_children.txt"

words = {}
wordpop = {}
maxpop = 0
maxlen = 0
maxscore = 0
setwords = set()
title = "Unknown"
ebookID = "Unknown"

def process_book(t):
    with open(t) as f:
        global maxpop, maxlen, maxscore, title, ebookID
        l = f.readline()
        # skip to the start of the book past the ebook spiel
        while not l.startswith("*** START"):
            if l.startswith("Title: "):
                title = l.strip().split(" ",1)[1:][0]
            elif "EBook #" in l:
                ebookID = l.strip().split()[-1][:-1]
            l = f.readline()
        l = f.readline() # get rid of the *** START line
        
        terminal = True
        last = ""
        i = 0
        for l in f:
            l = l.strip()
            # don't pollute with the boilerplate
            if l.startswith("*** END OF THIS PROJECT GUTENBERG"):
                break
            if not l:
                continue
            for w in l.split():
                w = w.lower()
                bare = w.strip(punctuation+" \t0123456789'\"-_")
                if not bare.isalpha(): # skip non-words
                    continue
                wl = len(w)
                cl = len([x for x in w if x.isalpha()])
                if float(cl) / wl < 0.5: # probably gibberish if more than half chars are non-alpha
                    continue
                
                if terminal: # start of a sentence
                    terminal = False
                else: # last word wasn't terminal
                    if last not in words:
                        words[last] = []
                    words[last].append(w)
                if bare not in wordpop:
                    wordpop[bare] = 1
                else:
                    wordpop[bare] += 1
                if len(bare) > maxlen:
                    maxlen = len(bare)
                sw = scoreWord(bare)
                if sw > maxscore:
                    maxscore = sw
                
                terminal = w[-1] in "!?."
                if not terminal:
                    setwords.add(w)
                last = w
        maxpop = max(wordpop.values())

def get_sentence():
    w = choice(list(setwords))

    i = 0
    out = [w]
    while i <= maxWords:
        if w[-1] in ".!?":
            break
        try:
            nxt = choice(words[w])
            w = nxt
        except IndexError:
            break # empty set of words
        out.append(nxt)
        i += 1
    return out

def scoreWord(w):
    total = 0
    for c in w:
        total += list(alc).index(c) if c in alc else 0
    return total

#-----------------------ANIMATION SECTION---------------------------------

lines = []
#    0     1      2                            3    4   5   6    7    8
#    x     y      z                            cx   cy  cz  upx, upy, upz
cam = [400, 800, 400, 400, 0, -400, 0,    1,   0]

# animation states
current_state = "growing"

vert_increment = 5
move_target = None
move_y = 0
pause_duration = 30 # frames
pause_frame = 0 # when pause started
current_sentence = []
displayed_words = [] # current sentence up to now
current_word = None

class Choice:
    def __init__(self, x, y, l, mh, a, col=(0,0,0)):
        self.x = x
        self.y = y
        self.l = l # length
        self.h = 0 # current height
        self.mh = mh # max height
        self.a = a # angle offset
        self.dst = a # destination offset angle when reorienting
        self.a_inc = 0 # amount to move each tick when reorienting
        self.col = col
    
    def grow(self, amount=1, perc=False):
        if self.h < self.mh:
            if perc: # grow by a percentage of max height
                self.h += (self.mh * float(amount))
            else: # grow by a fixed amount
                self.h += amount
        if self.h > self.mh:
            self.h = self.mh
    
    def target_angle(self, angle, inc): # target angle and number of increments
        self.dst = angle
        self.a_inc = (angle - self.a) / float(inc)
        #print("{} -> {} by {} x {}".format(self.a, angle, self.a_inc, inc))
    
    def reorient(self):
        # reorient to the destination angle
        if self.a == self.dst:
            return
        if (self.a_inc < 0 and self.a < self.dst) or (self.a_inc > 0 and self.a > self.dst):
            self.a = self.dst
            return
        self.a += self.a_inc
    
    def move(self):
        # move off screen
        self.y += vert_increment
    
    def draw_me(self):
        pushMatrix()
        fill(*self.col)
        stroke(0, 0, 0, 0.5)
        translate(self.x, self.y, 0)
        rotateZ(self.a)
        beginShape()
        vertex(0, 0, 0)
        vertex(0, self.l, 0)
        vertex(0, self.l, self.h)
        vertex(0, 0, self.h)
        endShape(CLOSE)
        popMatrix()

def regen_choices():
    global current_state, lines, current_word, maxpop
    lines = []
    
    current_word = current_sentence.pop(0)
    bare_word = current_word.strip(punctuation+" \t0123456789_-'\"")
    displayed_words.append(bare_word)
    if len(current_sentence) == 0:
        return
    
    branches = set(words[current_word])
    
    for i, w in enumerate(branches):
        # change max height to word popularity
        bw = w.strip(punctuation+" \t0123456789_-'\"")
        word_pop = (float(wordpop[bw]) / maxpop)
        c = Choice(400, 400, 100, word_pop * 100, ((i * PI/(len(branches)-1)) if len(branches)>1 else 0) + HALF_PI, col=(random(360), 0.5, 0.5, 0.4))
        lines.append(c)
    lines.sort(key=lambda x: x.mh)
    current_state = "growing"

def setup():
    global current_sentence
    size(800, 800, P3D)
    colorMode(HSB, 360, 1, 1, 1)
    
    randomSeed(rs)
    seed(rs)
    
    process_book(book)
    print("Book processed.")
    
    current_sentence = get_sentence()
    print(current_sentence)
    
    frameRate(30)
    
    regen_choices()
    print("Current sentence is: "+" ".join(current_sentence))

def draw():
    global current_state, lines, move_target, move_y, pause_frame, pause_duration
    background(0, 0, 1)
    camera(*cam)
    
    pushMatrix()
    textSize(32)
    textAlign(CENTER)
    fill(0)
    rotateX(-QUARTER_PI)
    text(title, width/2, -160)
    textSize(15)
    text("EBook ID: {}, Seed: {}".format(ebookID, rs), width/2, -140)
    popMatrix()
    
    if current_state == "growing":
        for c in lines:
            c.grow(amount=.05, perc=True) # grow 5% of max height per frame
            c.draw_me()
        # draw a dashed trail up to the current position
        pushMatrix()
        translate(400, 400, 0)
        for i in range(350/vert_increment): # draw a dashed line
            if i%2 == 1:
                line(0, vert_increment*(i-1), 0, vert_increment*i)
        popMatrix()
        
        if c.h == c.mh: # check if the lines have finished growing
            current_state = "choosing"
            
            next_choice = choice(lines)
            move_target = next_choice
            a_off = PI - next_choice.a
            for l in lines:
                l.target_angle(a_off + l.a, 30)
    
    # choosing a path, so re-orient the fan to the chosen word
    elif current_state == "choosing":
        for c in lines:
            c.reorient()
            c.draw_me()
        
        if c.a == c.dst:
            current_state = "chosen"
            move_y = 0
            
    
    # chosen a path, move to the end of the fan, then print the word
    elif current_state == "chosen":
        for c in lines:
            c.move()
        for c in lines:
            c.draw_me()
        move_y += vert_increment
        
        if move_y >= move_target.l:
            current_state = "show_word"
            pause_frame = frameCount
    # pause for a bit to show the current word
    elif current_state == "show_word":
        pass
        
        for c in lines:
            c.draw_me()
        
        pushMatrix()
        translate(400, 400, 0)
        rotateX(-QUARTER_PI)
        fill(0)
        textAlign(CENTER, CENTER)
        textSize(25)
        if len(current_sentence):
            text(current_sentence[0].strip(punctuation+" \t0123456789_-"), 0, -130, 50)
        else:
            text(".", 0, -130, 50)
        popMatrix()
        
        if frameCount > (pause_frame + pause_duration):
            current_state = "moving"
            move_y = 0
    # finished with the word, add it to the sentence and move the fan
    # off screen
    elif current_state == "moving":
        pushMatrix()
        translate(400, 400, 0)
        for i in range(move_y/vert_increment): # draw a dashed line
            if i%2 == 1:
                line(0, vert_increment*(i-1), 0, vert_increment*i)
        popMatrix()
        for c in lines:
            c.move()
        move_y += vert_increment
        for c in lines:
            c.draw_me()
        
        if move_y >= 350:
            current_state = "growing"
            regen_choices()
    
    # draw the current sentence to the screen, need to check length and figure out if we need to wrap it
    pushMatrix()
    rotateX(-QUARTER_PI)
    fill(0)
    textAlign(CENTER, CENTER)
    textSize(15)
    text(" ".join(displayed_words), width/2, -100, 0)
    popMatrix()
    
    if recording:
        saveFrame("frames/#####.png")
    
    if len(current_sentence) == 0:
        print("Finished.")
        noLoop()
            
    

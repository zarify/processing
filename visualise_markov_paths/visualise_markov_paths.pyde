from string import punctuation
from string import ascii_lowercase as alc
from random import choice, randint, seed

w, h = 1000, 1000
maxLength = 25.0 # contribution max line segment length
minLength = 25.0
maxWeight = 1.0 # contribution to max weight
minWeight = 1.0
weightMultiplier = 2
maxWords = 50 # max sentence length to be generated

drawWords = True

# draw a series of lines representing the different options
# then start the next word from the end of the chosen option, making a tree
# structure at each word choice

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
                bare = w.strip(punctuation+" \t0123456789")
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

def draw_sentence(s, x, y):
    global maxpop, maxsize

    for p, w in enumerate(s):
        # do this for each word in this word's chain, except for the first word's
        # so base it off p-1
        if p == 0:
            l = [w.strip(punctuation+" \t0123456789")]
        else:
            # pw = s[p-1].strip(punctuation+" \t0123456789")
            pw = s[p-1]
            l = set(words[pw]) # look at the potential words that go us here
        
        # angle stuff
        angleDiv = (HALF_PI / len(l)) % HALF_PI
        tick = -1 # left and right of PI divisor
        
        
        for i, lw in enumerate(l):
            lw = lw.strip(punctuation+" \t0123456789")
            word_pop = (float(wordpop[lw]) / maxpop) # word popularity as percentage
            word_score = scoreWord(lw) / float(maxscore) # word score as percentage
            word_len = len(lw) / float(maxlen) # word length as percentage of max word length
        
            weight = minWeight + word_pop * maxWeight * weightMultiplier # popularity determines weight of line
            col = hsbToRGB(word_score * 360, 0.8, 0.8) # word score determines colour
            linesize = minLength + word_len * maxLength # word length determines length of line segment
            
            stroke(*col)
            strokeWeight(weight)
            
            a = HALF_PI - (((i) * angleDiv) % HALF_PI)
            # flip x offset if i > half len(l)
            x_off = linesize * cos(a) * tick
            tick *= -1 # tock
            y_off = sqrt(linesize**2 - x_off**2)
            nx, ny = x + x_off, y + y_off
            
            line(x, y, nx, ny)
            
            stroke(100)
            strokeWeight(0.5)
            noFill()
            circle(x, y, 5)
            
            
            
            # does this need to be the next stem point?
            if lw == w.strip(punctuation+" \t0123456789"):
                tx, ty = nx, ny
        if drawWords:
            textSize(8)
            fill(0)
            text(lw, x, y - 5)

        x, y = tx, ty

        

def hsbToRGB(h, s, b):
    c = b * s
    x = c * (1 - abs((h/60) % 2 - 1))
    m = b - c
    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return ((r+m)*255, (g+m)*255, (b+m)*255, 100)

def setup():
    size(w, h)
    background(255)
    
    process_book(book)
    
    noLoop()
    noStroke()
    
def draw():
    rs = randint(0, 10000)
    
    textSize(32)
    textAlign(CENTER)
    fill(0)
    text(title, width/2, 40)
    textSize(15)
    text("EBook ID: {}, Seed: {}".format(ebookID, rs), width/2, 60)
    
    seed(rs)
    
    s = get_sentence()
    
    draw_sentence(s, width/2, 100)
    
    print("Done")
    save("markov.png")

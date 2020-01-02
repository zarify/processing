from string import punctuation
from string import ascii_lowercase as alc
from random import choice, randint, seed

w, h = 1000, 1000
maxsize = 300.0 # max line segment length

book = "books/modern_american_drinks.txt"

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

    maxwords = 50 # max length just in case, don't want huge sentences
    i = 0
    out = [w]
    while i <= maxwords:
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
    
    angle = 0

    for p, w in enumerate(s):
        word_pop = (float(wordpop[w.strip(punctuation+" \t0123456789")]) / maxpop) # word popularity as percentage
        word_score = scoreWord(w) / float(maxscore) # word score as percentage
        word_len = len(w) / float(maxlen) # word length as percentage of max word length
        
        new_angle = angle + word_pop * TWO_PI # popularity determines length of arc
        col = hsbToRGB(word_score * 360, 0.8, 0.8) # word score determines colour
        arcsize = word_len * maxsize # word length determines size of arc
        
        fill(*col)
        
        arc(x, y, arcsize, arcsize, angle, new_angle, PIE)
            
        angle = new_angle % TWO_PI
        
        

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
    
    xoff = (width - int(width/maxsize)*maxsize) / 2
    yoff = (height - int(height/maxsize)*maxsize) / 2
    for yi in range(int(height/maxsize)):
        for xi in range(int(width/maxsize)):
            s = get_sentence()
            draw_sentence(s, xi * maxsize + xoff + maxsize/2, yi * maxsize + yoff + maxsize/2)
    print("Done")
    save("markov.png")

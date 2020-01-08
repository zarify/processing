from string import punctuation
from string import ascii_lowercase as alc
from reportTime import reportTime

w, h = 1600, 800
maxsize = 500.0 # max line segment length
z_inc = 0.05

fall_away = True # lower layers fall away by accelerating their z change the lower they get
accel_amount = 0.005
fall_thresh = 300

recording = False # save frames

maxFrames = 3000

cam = [w/2.0,                           # 0 - eye x (w/2.0)
       1000,                           # 1 - eye y (h/2.0)
       300,                             # 2 - eye z ((h/2.0) / tan(PI*30.0 / 180.0))
       w/2.0,                           # 3 - center x (w/2.0)
       h/2.0,                           # 4 - center y (h/2.0)
       0,                               # 5 - center z (0)
       0,                               # 6 - up x (0)
       1,                               # 7 - up y (1)
       0]                               # 8 - up z (0)

book = "books/christmas_carol" # middle
book1 = "books/frankenstein" # left
book2 = "books/holmes" # right

global_len = 0
global_score = 0

book_data = {}

moby_freq = []
stop_words = []

def setup_book(name, x, y):
    book_data[name] = {
                "wordpop": {},           # word populations
                "sentences": [],         # sentences to process
                "toDraw": [],            # previously processed words
                "maxpop": 0,             # word count of most popular word
                "maxlen": 0,             # length of longest word
                "maxscore": 0,           # 'score' of highest scoring word
                "setwords": set(),       # set of unique words
                "title": "Unknown",      # title of the book
                "ebookID": "Unknown",    # Project Gutenberg ID
                "angle": 0,              # current arc angle
                "w_index": 0,            # current word index in sentence
                "s_index": 0,            # current sentence index into sentences list
                "cx": x,                 # arc center coordinates
                "cy": y,
                "cz": 0,                 # current z height
                "sen_col": 0.0           # colour of the current sentence
                       }

def loadMoby():
    """
    Loads up the most common words list from the Moby Word Lists: http://www.gutenberg.org/ebooks/3201
    """
    with open("files/FREQ.TXT") as moby:
        for l in moby:
            moby_freq.append(l.strip("\n \t"))

def loadStopWords():
    """
    http://xpo6.com/download-stop-word-list/
    """
    with open("files/stop-word-list.txt") as stop:
        global stop_words
        stop_words = stop.read().strip().split("\n")

def drawTitle(t):
    """
    Title and eBook ID from the Project Gutenberg file, drawn at the base of each column.
    Be nice to make them face the camera rather than facing up, but meh, it's readable.
    """
    pushStyle()
    pushMatrix()
    rotateX(radians(-55))
    curr_z = book_data[t]["cz"] + 300
    translate(book_data[t]["cx"], book_data[t]["cy"]-2*maxsize/3, curr_z)
    fill(0)
    textSize(26)
    textAlign(CENTER)
    text(book_data[t]["title"], 0, 0)
    textSize(18)
    text("EBookID: "+book_data[t]["ebookID"], 0, 25)
    popMatrix()
    popStyle()

def process_book(t):
    """
    Open a Project Gutenberg book and process each of the sentences, finding the length of the
    longest word in the book, as well as the population of each word encountered.
    """
    with open(t) as f:
        global global_len, global_score
        l = f.readline()
        # skip to the start of the book past the ebook spiel
        while not l.startswith("*** START"):
            if l.startswith("Title: "):
                book_data[t]["title"] = l.strip().split(" ",1)[1:][0]
            elif "EBook #" in l:
                book_data[t]["ebookID"] = l.strip().split()[-1][:-1]
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
                if bare in stop_words:
                    continue
                if not bare.isalpha(): # skip non-words
                    continue
                wl = len(w)
                cl = len([x for x in w if x.isalpha()])
                if float(cl) / wl < 0.5: # probably gibberish if more than half chars are non-alpha
                    continue
                
                if terminal: # start of a sentence
                    terminal = False
                    book_data[t]["sentences"].append([]) # new list for this sentence
                if bare not in book_data[t]["wordpop"]:
                    book_data[t]["wordpop"][bare] = 1
                else:
                    book_data[t]["wordpop"][bare] += 1
                book_data[t]["sentences"][-1].append(bare) # add word to current sentence
                
                if len(bare) > book_data[t]["maxlen"]:
                    book_data[t]["maxlen"] = len(bare)
                if len(bare) > global_len:
                    global_len = len(bare)
                
                terminal = w[-1] in "!?."
                if not terminal:
                    book_data[t]["setwords"].add(w)
                last = w
        book_data[t]["maxpop"] = max(book_data[t]["wordpop"].values())

def scoreWord(w):
    """
    Score words by their position in the Moby word frequency list as a
    percentage.
    """
    try:
        return 1.0 - moby_freq.index(w) / len(moby_freq)
    except:
        return 0.0

def drawNext(t):
    """
    Calculate and draw the next word's arc, as well as pushing it onto the toDraw list
    for this book to be drawn in the future as the camera moves up.
    """
    si = book_data[t]["s_index"]
    wi = book_data[t]["w_index"]
    
    try:
        # I honestly don't know why I'm stripping spaces here, since they will already
        # be gone after splitting on them :P
        w = book_data[t]["sentences"][si][wi].strip(punctuation+" \t0123456789")
    except IndexError:
        return True
    
    word_pop = float(book_data[t]["wordpop"][w]) / book_data[t]["maxpop"]
    word_score = scoreWord(w)
    word_len = len(w) / float(global_len)
    
    new_angle = book_data[t]["angle"] + word_pop * TWO_PI # popularity determines length of arc
    col = hsbToRGB(book_data[t]["sen_col"], word_score * 0.6 + 0.4, 0.8) # word score determines colour 
    arcsize = word_len * maxsize # word length determines radius of arc
    
    fill(*col)
    #pushMatrix()
    #translate(0, 0, book_data[t]["cz"])
    
    arc(book_data[t]["cx"], book_data[t]["cy"], arcsize, arcsize, book_data[t]["angle"], new_angle, PIE)
    book_data[t]["toDraw"].append([[book_data[t]["cx"], book_data[t]["cy"], arcsize, arcsize, book_data[t]["angle"], 
                                    new_angle, PIE], book_data[t]["cz"], col])
    #popMatrix()
    
    #book_data[t]["cz"] += z_inc
    book_data[t]["angle"] = new_angle % TWO_PI
    
    book_data[t]["w_index"] += 1
    if book_data[t]["w_index"] >= len(book_data[t]["sentences"][book_data[t]["s_index"]]):
        # change the sentence colour at the end of the current sentence
        book_data[t]["w_index"] = 0
        book_data[t]["s_index"] += 1
        book_data[t]["sen_col"] = (book_data[t]["sen_col"] + 10) % 360

    return book_data[t]["s_index"] >= len(book_data[t]["sentences"])

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
    size(w, h, P3D)
    background(255)
    
    loadMoby()
    loadStopWords()
    
    setup_book(book, w/2.0, h/2)
    process_book(book)
    
    setup_book(book1, w/4.0, h/2)
    process_book(book1)
    
    setup_book(book2, 3*w/4.0, h/2)
    process_book(book2)
    
    for b in book_data:
        print("Title: {}".format(book_data[b]["title"]))
        print("\t{} sentences.".format(len(book_data[b]["sentences"])))
        print("\t{} total words.".format(sum(map(len, book_data[b]["sentences"]))))
    
    #frameRate(20)
    
    camera(*cam)
    
    stroke(100, 100, 100, 50)
    strokeWeight(0.5)
    
def draw():
    global book_data
    
    if frameCount % 100 == 0:
        print("Frame {}".format(frameCount))
        drawqueue = 0
        for b in book_data:
            drawqueue += len(book_data[b]["toDraw"])
        print("Current queue length: {}".format(drawqueue))
        reportTime()
    
    
    background(255)
    
    for b in book_data:
        # draw old arcs
        drawTitle(b)
        ltd = len(book_data[b]["toDraw"])
        for i, dq in enumerate(book_data[b]["toDraw"]):
            arcdef, z, col = dq
            pushMatrix()
            if (ltd - i) > fall_thresh:
                z -= accel_amount * (ltd - fall_thresh - i)
            else:
                z -= z_inc
            book_data[b]["toDraw"][i][1] = z
            translate(0, 0, z)
            fill(*col)
            arc(*arcdef)
            popMatrix()
        
        # prune arcs which are too far away so the list doesn't get too large later on
        book_data[b]["toDraw"] = [x for x in book_data[b]["toDraw"] if x[1] > (book_data[b]["cz"] - 400)]
        
        lastWord = drawNext(b)
    
    if recording:
        saveFrame("frames/######.jpg")
    
    if lastWord or frameCount >= maxFrames:
        reportTime()
        save("visualise.png")
        noLoop()
        print("Done")

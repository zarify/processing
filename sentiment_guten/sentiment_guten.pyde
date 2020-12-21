from sentiment import analyse

# add in my analysis stuff from the project gutenburg
# bubbles across the screen as sentences are processed?
# !!! or maybe a sentiment graph using lines?
# would be neat to also have the sentiment words to pop in and fade out as they are processed
# too, maybe just one at random from each sentence, word cloud style

from string import punctuation
from string import ascii_lowercase as alc
from reportTime import reportTime

w, h = 1600, 800
maxsize = 500.0 # max line segment length
 
mid_line = (h-200)/2 # y=0 axis for graph
max_height = mid_line * 0.8 # max graph length

stroke_width = 5.0
fade = 3.0

recording = False # save frames

maxFrames = 3000

book = "books/christmas_carol"

max_score = 0 # maximum sentence score
min_score = 0 # minimum sentence score

book_data = {}
splash_words = {} # words: {"colour": [r, g, b, a], "location": [x,y]}

def setup_book(name, x, y):
    book_data[name] = {
                "sentences": [],         # sentences to process, replaced by scored words and sentence score when done
                "scored_sentences": [],
                "title": "Unknown",      # title of the book
                "ebookID": "Unknown",    # Project Gutenberg ID
                "s_index": 0,            # current sentence index into sentences list
                "cx": x,
                "cy": y,
                       }

def drawTitle(t):
    """
    Title and eBook ID from the Project Gutenberg file, drawn at the base of each column.
    Be nice to make them face the camera rather than facing up, but meh, it's readable.
    """
    pushStyle()
    pushMatrix()
    translate(book_data[t]["cx"], book_data[t]["cy"])
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
        # process each line in the file
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
                    book_data[t]["sentences"].append([]) # new list for this sentence
                book_data[t]["sentences"][-1].append(w) # add word to current sentence
                
                terminal = w[-1] in "!?."
                last = w

def score_book(t):
    global max_score, min_score
    for sentence in book_data[t]["sentences"]:
        score, scored_words = analyse(" ".join(sentence))
        if score > max_score:
            max_score = score
        if score < min_score:
            min_score = score
        book_data[t]["scored_sentences"].append((score, scored_words))
    print("Min: {}, Max: {}".format(min_score, max_score))

def drawNext(t):
    """
    Draw a vertical line for the current sentence being processed, and all sentences
    up to that point.
    """
    ci = book_data[t]["s_index"]
    visible = int((width / 2) / stroke_width) # number of visible lines marching left
    stop = visible if ci >= visible else ci
    
    # check if we add in a splash word from the current sentence only
    if random(1) > 0.9:
        sw = [b for b in book_data[t]["scored_sentences"][ci][1] if book_data[t]["scored_sentences"][ci][1][b] != 0]
        if sw:
            rw = sw[int(random(len(sw)))]
            ws = book_data[t]["scored_sentences"][ci][1][rw]
            splash_words[rw] = { "colour": [200 if ws < 0 else 0, 200 if ws > 0 else 0, 0, 255],
                                "location": [random(width-200)+200, random(100)+50 + (0 if ws > 0 else mid_line + 100)],
                                "score": ws }
            # print("added {} {}".format(rw, splash_words[rw]))
    
    # draw each of the sentences up to now
    for i in range(stop):
        score, scored_words = book_data[t]["scored_sentences"][ci-i]
        if score < 0:
            line_len = float(score) / min_score * max_height
        elif score > 0:
            line_len = float(score) / max_score * max_height
        else:
            line_len = 0

        lx = width/2 - i * stroke_width # this needs to be relative to the screen not sentence index
        strokeWeight(stroke_width)
        if score > 0:
            stroke(0,float(score) / max_score * 100 + 155,0)
        elif score < 0:
            stroke(float(score) / min_score * 100 + 155,0,0)
        if line_len:
            line(lx, mid_line, lx, mid_line - line_len * (-1 if score < 0 else 1))
    
    book_data[t]["s_index"] += 1
    if book_data[t]["s_index"] >= len(book_data[t]["scored_sentences"]):
        return True
    else:
        return False                    

def splashWords():
    """
    Draw the random selection of scored words on the screen until they fade away.
    """
    pushStyle()
    for word in splash_words:
        fill(*splash_words[word]["colour"])
        textSize(30 + abs(splash_words[word]["score"]) / 4.0 * 25)
        textAlign(CENTER)
        text(word, splash_words[word]["location"][0], splash_words[word]["location"][1])
        splash_words[word]["colour"][3] -= fade
        if splash_words[word]["colour"][3] <= 0:
            del splash_words[word]
    popStyle()

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
    
    setup_book(book, width/2.0, height-50)
    process_book(book)
    score_book(book)
    
    for b in book_data:
        print("Title: {}".format(book_data[b]["title"]))
        print("\t{} sentences.".format(len(book_data[b]["sentences"])))
    
    #frameRate(10)
    #noLoop()
    
    stroke(100, 100, 100, 50)
    strokeCap(SQUARE)
    strokeWeight(0.5)
    
def draw():
    global book_data, mid_line
    
    if frameCount % 100 == 0:
        print("Frame {}".format(frameCount))
        reportTime()
    
    
    background(255)
    pushStyle()
    strokeWeight(1)
    stroke(0)
    line(0,mid_line,width,mid_line)
    popStyle()
    
    for b in book_data:
        drawTitle(b)
        lastSentence = drawNext(b)
    splashWords()
    
    if recording:
        saveFrame("frames/######.jpg")
    
    if lastSentence or frameCount >= maxFrames:
        reportTime()
        save("visualise.png")
        noLoop()
        print("Done")

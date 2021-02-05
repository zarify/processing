# Increase the randomness along the Y-axis.
# Start with a line from song lyrics, have a bouncing ball go down the page, make the
# words more chaotic:
#    similar length words starting and ending with the same letters
#    shuffle random letters around
#    shuffle word order

from p5 import *
from random import randint, shuffle, choice, random
from math import sin, cos, pi
import json
from string import ascii_lowercase as a_l
from string import punctuation as punc
import requests

# PROFILING
import cProfile
import io
import pstats

def profile(func):
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = func(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = "cumulative" #SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval
    return wrapper
# END PROFILING

# Word functions

def process_words(words):
    # turn the words dict into a sorted: [list of same words] dict instead
    global processed
    processed = {}
    for w in words:
        sw = "".join(sorted(w))
        if sw not in processed:
            processed[sw] = []
        processed[sw].append(w)

def word_dist(w1, w2):
    # return the distance between w1 and w2 in terms of changed letters
    # or length of the words
    d = 0
    # take away any letters the words do not have in common
    # then compare what's left
    w1s, w2s = set(w1), set(w2)
    d += len(w1s ^ w2s)

    # now check for how many swapped letters
    # of the letters they have in common
    for c1, c2 in zip(w1, w2):
        if c1 != c2:
            d += 1
    else:
        d += abs(len(w1)-len(w2))
    return d

def swap_letters(w):
    # randomly swap letters within w and return a list of potential variants
    perms = []
    for i in range(len(w)-1):
        if w[i] != w[i+1]:
            perms.append(w[:i]+w[i+1]+w[i]+w[i+2:])
    return perms

def grow_shrink(w):
    # grow or shrink w by one letter, making valid words if possible
    perms = []
    variants_grow = [sorted(w+c) for c in a_l]
    if len(w) > 3:
        variants_shrink = [sorted(w[:i]+w[i+1:]) for i in range(len(w))]
    else:
        variants_shrink = []
    
    for word in variants_grow + variants_shrink:
        word = "".join(word)
        if word in processed:
            for potential in processed[word]:
                if word_dist(w, potential) < 4:
                    perms.append(potential)
    return perms

def get_perm(w):
    # get permutations of w where permutations may be one letter
    # difference (changed, added, removed)
    perms = set()
    sw = "".join(sorted(w))
    if sw in processed:
        for p in processed[sw]:
            if word_dist(w, p) < 3 and w != p: # change to legit words if possible
                perms.add(p)
            else: # otherwise swap a random letter
                perms |= set(swap_letters(w)) 
            perms |= set(grow_shrink(w)) # always be able to grow/shrink
    return perms

def change_sentence(s):
    # make one change to s and return the modified sentence
    words = s.split()
    pos = int(random()*len(words))
    potentials = get_perm(words[pos])
    while len(potentials) == 0:
        pos = int(random()*len(words))
        potentials = get_perm(words[pos])
    new_word = choice(list(potentials))
    words[pos] = new_word
    return " ".join(words)

# Display functions
# Sentence display
s_x_off = 120
s_y_off = 100
s_line_height = 80
sentences = []
# Bouncing ball
b_x_off = 40
b_y_off = s_line_height
b_r = s_line_height/2
ball_rate = 100 # how many frames per bounce
ball_radius = 30

background_lines = []
background_shapes = []

def show_sentences():
    # sentence, lines from top
    text_align("LEFT", "CENTER")
    fill(0)
    no_stroke()
    for i, s in enumerate(sentences):
        text(s, s_x_off, s_y_off + i * s_line_height)

def draw_ball():
    no_stroke()
    seg_a = pi / ball_rate
    a_off = - pi # start angle
    a = (a_off + (seg_a * frame_count % ball_rate)) % pi - pi/2
    x = cos(a) * b_r + b_x_off
    y = sin(a) * b_r + b_y_off/2 + (b_r*2) * (frame_count // ball_rate + 1)
    fill(0, 1, 1)
    circle(x, y, ball_radius)
    fill(0,0,1,0.7)
    circle(x-ball_radius/5, y-ball_radius/5, ball_radius/3)

def draw_busy():
    stroke(0, 0, 0, 0.1)
    for w, l in background_lines:
        stroke_weight(w)
        line(*l)
    
    no_stroke()
    for c, s in background_shapes:
        fill(*c)
        begin_shape()
        for x, y in s:
            vertex(x, y)
        end_shape("CLOSE")

def add_busy():
    if random() > 0.8: # poly
        c = (random()*360, random()*0.3+0.3, random()*0.3+0.5, random()*0.1+0.1)
        p = int(random()*3)+3
        points = []
        for i in range(p):
            points.append((random()*width, random()*height))
        background_shapes.append((c, points))
    else: # line
        background_lines.append((random()*2+0.5, ((random()*width,random()*height),(random()*width,random()*height))))

def setup():
    global lyric
    size(800, 800)
    color_mode('HSB', 360, 1, 1, 1)
    
    f = create_font("arial.ttf", 24)
    text_font(f)

    with open("words_dictionary.json") as f:
        words = json.load(f)
        process_words(words)
    
    r = requests.get("https://api.kanye.rest/?format=text")
    r_str = " ".join([x.strip(punc) for x in str(r.content).strip("\"b'").lower().split()])
    
    sentences.append(r_str)

#@profile
def draw():
    background(0, 0, 1)
    draw_busy()
    no_fill()
    stroke(0)
    stroke_weight(10)
    rect(0, 0, width, height)
    
    if frame_count % 20 == 0:
        add_busy()
    
    draw_ball() # bounce the ball down the left side of the screen
    if frame_count % ball_rate == 0:
        times = len(sentences)
        ls = sentences[-1]
        for i in range(times):
            ls = change_sentence(ls)
        sentences.append(ls)
    show_sentences()
    
    save_frame("d:/tmp/frames/d19.png")
    if (len(sentences) * s_line_height + s_y_off) > (height - s_line_height):
        no_loop()
        print("Done.")
        exit()

run()
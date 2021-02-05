
from random import randint, shuffle, choice, random
from math import sin, cos
import json
from string import ascii_lowercase as a_l

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
    new_word = choice(list(potentials))
    words[pos] = new_word
    return " ".join(words)

def setup():
    global lyric

    
    with open("words_dictionary.json") as f:
        words = json.load(f)
        process_words(words)
    
    lyric = "rob orbit poulter"

setup()

for i in range(10):
    print(lyric)
    lyric = change_sentence(lyric)
print(lyric)


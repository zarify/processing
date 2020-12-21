# import our list of stop words
from stopwords import stop_words

word_list = {} # word: strength, +ve -ve numbers for polarity
print("Loading word list...")
with open("subjclues.txt") as f:
    line = f.readline().strip("\n")
    while line:
        pairs = line.split(" ")
        # 0, 2, -1
        polarity_type = pairs[0].split("=")[1]
        word = pairs[2].split("=")[1]
        strength = pairs[-1].split("=")[1]
        mod = 1
        if strength == "negative":
            mod *= -1
        if polarity_type == "strongsubj":
            mod *= 2
        word_list[word] = mod
        line = f.readline().strip("\n")
print("Word list loaded ({} words)".format(len(word_list)))
# customise good/bad for context
def add_word(word, weight):
    if word not in word_list:
        word_list[word] = weight
    else:
        print("Warning: {} is already in word list with weighting {}.".format(word,word_list[word]))

def remove_word(word):
    if word in word_list:
        del word_list[word]
    else:
        print("Warning: {} not found in word list.".format(word))

# customise word list
# e.g. add_word("buy", 1)
# e.g. remove_word("really")
remove_word("really")
remove_word("just")
remove_word("incredibly")

# local modifiers
inverters = ["not", "isn't", "can't", "didn't", "don't", "no"]
amplifiers = ["really", "incredibly", "very", "always"]
minimisers = ["slightly", "little", "partly", "somewhat"]

for word in amplifiers + minimisers:
    if word in word_list:
        remove_word(word)
    if word in stop_words:
        stop_words.remove(word)

# function for passing in sentences
def analyse(sentence):
    score = 0
    words = [w for w in sentence.split() if w.lower().strip(",.?!") not in stop_words]
    scored_words = {} # word: score
    for i, word in enumerate(words):
        wordscore = 0
        norm_word = word.lower().strip(",.?!")
        if norm_word in word_list:
            wordscore += word_list[norm_word]
            #print(f"{norm_word} {wordscore}") # this is useful for debugging!
        if i != 0 and words[i-1].lower().strip(",.?!") in inverters:
            wordscore *= -1
        
        # PUT AMPLIFIER CODE HERE
        if i != 0 and words[i-1].lower().strip(",.?!") in amplifiers:
            wordscore *= 2
        
        # Local Caps Rule - what do we need to think about here?
        if word.isupper() and not sentence.isupper():
            wordscore *= 1.5
        
        score += wordscore
        scored_words[norm_word] = wordscore
    # check if the whole sentence is in caps
    if sentence.isupper():
        score *= 2 # score = score * 2
    # check if the last character is !
    if sentence[-1] == "!":
        score *= 2
    
    return score, scored_words

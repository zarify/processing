"""
Helper functions to introduce noise (grain) to specific colours within an
image within a specified tolerance (default 10% of original HSB values)
"""

def close_enough(col1, col2, thresh):
    hp = abs((col1[0] - col2[0])/360.0) <= thresh
    sp = abs((col1[1] - col2[1])) <= thresh
    bp = abs((col1[2] - col2[2])) <= thresh
    return hp and sp and bp

def random_noise(thresh=0.95, amt=1.0, colours=[], similarity=0.1):
    loadPixels()
    colours = [[round(h, 2), round(s, 2), round(b, 2)] for h, s, b in colours]
    for i in range(width * height):
        x, y = i % width, int(i / width)
        h, s, b = round(hue(pixels[i]),2), round(saturation(pixels[i]),2), round(brightness(pixels[i]),2)
        close_colour = any([close_enough((h, s, b), c, similarity) for c in colours])
        if (not colours or close_colour):
            if random(1) > thresh:
                c = color(h, s, b + random(-amt, amt))
                pixels[i] = c
    updatePixels()

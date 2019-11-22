from random import randint, choice, seed

w, h = 800, 800

dirs = { "N": (0, -1),
         "NE": (1, -1),
         "E": (1, 0),
         "SE": (1, 1),
         "S": (0, 1),
         "SW": (-1, 1),
         "W": (-1, 0),
         "NW": (-1, -1)
        }
d_choices = {
             "N": ("NW", "N", "NE"),
             "NE": ("N", "NE", "E"),
             "E": ("NE", "E", "SE"),
             "SE": ("E", "SE", "S"),
             "S": ("SE", "S", "SW"),
             "SW": ("S", "SW", "W"),
             "W": ("SW", "W", "NW"),
             "NW": ("W", "NW", "N"),
             }

def worm(x, y, d, iter, max_iter, cs, col):
    sz = random(cs)+cs
    high_col = [c+50 for c in col]
    fill(*col)
    circle(x, y, sz)
    fill(*high_col)
    circle(x-sz/4, y-sz/4, sz/3.5)
    nd = choice(d_choices[d])
    x += dirs[nd][0] * sz/4
    y += dirs[nd][1] * sz/4
    d = nd
    
    if iter < max_iter:
        worm(x, y, d, iter + 1, max_iter, cs, col)

def setup():
    size(w, h)
    background(255, 255, 255)
    
    worms = randint(50, 150)
    
    noStroke()

    for i in range(worms):
        cs = randint(3, 10)
        d = choice(dirs.keys())
        x, y = random(w), random(h)
        max_iter = randint(100, 300)
        fc = randint(100, 200), randint(100, 200), randint(100, 200)
        
        worm(x, y, d, 0, max_iter, cs, fc)
    save("worms.png")

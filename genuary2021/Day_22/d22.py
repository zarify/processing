# draw a line, wrong answers only
# make little tunnels, have the lines go through them, do S curves with quadratics

# SOCIALISM
# healthcare, social security, education, human rights, living wage
from p5 import *
from math import sin, cos, pi
from random import choice, shuffle, randint

def tunnel(x, y, sz): # sz is radius of arc, centered on x, y of arc
    with push_style():
        no_stroke()
        with push_matrix():
            
            translate(x, y)
            fill(0, .57, .32)
            arc(0, 0, sz+10, sz*1.1+10, PI, 2*PI)
            rect(-sz/2-5, 0, sz+10, sz/2)
            fill(0)
            arc(0, 0, sz, sz*1.1, PI, 2*PI)
            rect(-sz/2, 0, sz, sz/2)
            

def tunnel_shadow(x, y, sz):
    # draw a shadow over whatever is entering/exiting the tunnel
    a = 0
    a_off = 1.0 / (sz/3)
    with push_style():
        no_stroke()
        with push_matrix():
            translate(x-sz/2, y+sz/2)
            for i in range(int(sz/3)):
                stroke(0, 0, 0, a)
                line((0,-i), (sz,-i))
                a += a_off

def setup():
    size(1000, 1000)
    color_mode('HSB', 360, 1, 1, 1)
    f = create_font("brlnsr.ttf", 24)
    text_font(f)
    
    no_loop()

def draw():
    background(199, 0.16, 0.29)
    track_colours = ((0, 1, 1), (140, 0.53, 0.55), (210, 0.79, 0.55), (23, 0.97, 0.85), (209, 0.61, 0.64), (49, .91, .52))
    words = ["HEALTH CARE", "EDUCATION", "SOCIAL SECURITY", "EQUALITY", "LIVING WAGE", "RESPECT"]
    shuffle(words)
    locs = (((130, 95), (290, 285)), # word loc, gate loc
            ((325, 635), (100, 415)),
            ((536, 692), (162, 906)),
            ((850, 915), (591, 916)),
            ((704, 441), (893, 705)),
            ((569, 288), (878, 112)),
            )
    paths = [ # set of quadratic paths to the gate
        ((130, 100), (132, 143), (191, 181), (313, 209), (363, 284), (324, 338), (292, 320), (289, 296)),
        ((325, 640), (294, 693), (183, 722), (96, 629), (137, 507), (98, 428)),
        ((536, 697), (534, 792), (469, 833), (418, 812), (428, 741), (489, 734), (507, 901), (412, 951), (311, 892), (206, 964), (161, 954), (160, 918)),
        ((850, 920), (866, 939), (925, 963), (976, 902), (918, 841), (783, 865), (699, 827), (647, 866), (681, 932), (644, 979), (595, 957), (590, 930)),
        ((704, 446), (704, 470), (744, 501), (784, 468), (828, 430), (872, 469), (835, 535), (784, 607), (729, 737), (863, 766), (893, 721)),
        ((569, 293), (512, 312), (428, 272), (450, 94), (388, 77), (388, 154), (700, 48), (759, 235), (697, 228), (723, 172), (868, 173), (879, 125)),
    ]
    word_colours = list(range(len(track_colours)))
    shuffle(word_colours)
    text_align("CENTER", "BOTTOM")
    for word, gate in locs:
        w = words.pop()
        p = paths.pop(0)
        fill(0, 0, 1)
        no_stroke()
        text_size(randint(28, 32))
        text(w, *word)
        tw = randint(40, 60)
        tunnel(*gate, tw)
        # DEBUG
        # stroke(0, 0, 1)
        # line(word, gate)

        # if len(p) == 2: # DEBUG
        #     continue
        stroke(*track_colours[word_colours.pop()])
        stroke_weight(6)
        no_fill()
        
        begin_shape()
        vertex(*p[0])
        vertex(*p[0])
        for x, y in p[1:-1]:
            curve_vertex(x, y)
            # with push_style(): # DEBUG
            #     fill(0, 1, 1)
            #     no_stroke()
            #     circle(x, y, 10)
        vertex(*p[-1])
        vertex(*p[-1])
        end_shape()

        tunnel_shadow(*gate, tw)

    #-------------- SOCIALISM!
    tunnel(500, 400, 70)
    # tracks coming out to text
    xtop_w = 5
    xbottom_w = 10
    xpad = 4
    xtop = ((500-(70/2))+((xtop_w+xpad/2)*len(track_colours)/8))
    ytop = 420
    xbottom = 530
    ybottom = 530
    tracks = []
    for i in range(len(track_colours)):
        track = (
            (xtop, ytop),
            (xtop+xtop_w, ytop),
            (xbottom+xbottom_w, ybottom),
            (xbottom, ybottom)
        )
        tracks.append(track)
        xtop += xtop_w + xpad/2
        xbottom += xbottom_w + xpad

    for c, points in zip(track_colours, tracks):
        fill(*c)
        no_stroke()
        begin_shape()
        for p in points:
            vertex(*p)
        end_shape(CLOSE)
    tunnel_shadow(500, 400, 70)
    with push_style():
        text_align("CENTER", "CENTER")
        fill(0)
        text_size(40)
        text("</S>OCIALISM!", 583, 553)
        fill(0, 1, 1)
        stroke(0)
        text_size(40)
        stroke_weight(2)
        text("</S>OCIALISM!", 580, 550)
    
    save("22.png")

def mouse_pressed():
    print(f"{mouse_x}, {mouse_y}")
    with push_style():
        no_stroke()
        fill(0, 1, 1)
        circle(mouse_x, mouse_y, 5)

run()
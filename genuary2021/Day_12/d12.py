import requests, json, datetime
from calendar import monthrange, isleap
from math import cos, sin, radians, pi, degrees
from p5 import *

# draw public holidays on a circle. The circle increases radius until it hits a public holiday
# and then resets to the starting radius
# Can do a montage of the different states

default_r = 70

circles = {} # state: circle
fills = [(209, 0.61, 0.64),
         (170, 0.61, 0.64),
         (56, 0.61, 0.64),
         (251, 0.61, 0.64),
         (0, 0.61, 0.64),
         (327, 0.61, 0.64),
         (105, 0.61, 0.64),
         (159, 0.61, 0.64)
    ]

class StateCircle:
    def __init__(self, x, y, r, year, label, col):
        self.x = x
        self.y = y
        self.label = label
        self.col = col
        self.radius = r
        self.days = [False for i in range(366 if isleap(year) else 365)]
        self.last_r = self.radius
    
    def populate(self, d):
        for day in d:
            i = days_in(day)
            self.days[i] = True
    
    def draw_me(self):
        da = (pi*2) / len(self.days)
        a_off = -pi/2
        stroke(0, 0, 0, 0.25)
        fill(*self.col)
        r = self.radius
        circle_coords = []
        begin_shape()
        for i, d in enumerate(self.days):
            if not d:
                r += 0.3
            else:
                r = self.radius
            x = cos(da*i+a_off)*r+self.x
            y = sin(da*i+a_off)*r+self.y
            vertex(x, y)
            if i == 0:
                push_style()
                fill(0, 1, 1)
                circle(x, y, 20)
                pop_style()
            if d:
                circle_coords.append((x, y))
        end_shape('CLOSE')
        fill(0, 0, 1)
        stroke(0, 0, 0, 0.25)
        for x,y in circle_coords:
            circle(x, y, 10)

def days_in(d):
    year, month, day = int(d[:4]), int(d[4:6]), int(d[6:])
    fromDate = datetime.date(year, 1, 1)
    toDate = datetime.date(year, month, day)
    return (toDate - fromDate).days

def draw_months(year):
    push_matrix()
    push_style()
    translate(width/2, height/2)
    rotate_z(-pi/2)
    months = [x for x in range(1,13)]
    aoff = (pi*2)/(366 if isleap(year) else 365)
    sumdays = 0
    monthnames = [None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for m in months:
        # draw a faint line to indicate this month cutoff
        halfmonth = monthrange(year, m)[1] / 2
        
        x, y = cos(aoff*sumdays)*width, sin(aoff*sumdays)*width
        
        push_matrix()
        push_style()
        fill(0,0,1)
        no_stroke()
        x1, y1 = 0, -height/2
        rotate_z(pi/2+aoff*(sumdays+halfmonth))
        text_align("CENTER", "CENTER")
        text(monthnames[m], x1, y1)
        pop_style()
        pop_matrix()
        
        sumdays += monthrange(year, m)[1]
        stroke(0, 0, 0, 0.2)
        line((0, 0), (x, y))
    pop_style()
    pop_matrix()

def get_data():
    datastore = "2dee10ef-2d0c-44a0-a66b-eb8ce59d9110"
    url = f"https://data.gov.au/data/api/3/action/datastore_search?resource_id={datastore}"
    f = requests.get(url)
    d = json.loads(f.content)
    if len(d["result"]["records"]) != d["result"]["total"]:
        url += f"&limit={d['result']['total']}"
        f = requests.get(url)
        d = json.loads(f.content)
    return d["result"]["records"]

def draw_legend():
    xoff = 15
    yoff = 15
    push_style()
    no_stroke()
    for c in circles:
        fill(*circles[c].col)
        circle(xoff, yoff, 15)
        fill(0, 0, 1)
        text_align("LEFT")
        text(circles[c].label.upper(), xoff+25, yoff)
        yoff += 20
    pop_style()

def setup():
    global year, f
    size(1200, 1000)
    color_mode('HSB', 360, 1, 1, 1)
    f = create_font("fonts/arial.ttf", 16)
    text_font(f)
    no_loop()
    
    d = get_data()
    year = int(d[0]['Date'][:4])
    rmult = 1.5
    col_idx = 0
    for state in sorted(set((x["Jurisdiction"] for x in d))):
        c = StateCircle(width/2, height/2, default_r * rmult, year, state, fills[col_idx])
        c.populate((x['Date'] for x in d if x["Jurisdiction"] == state))
        circles[state] = c
        rmult += 0.7
        col_idx += 1

def draw():
    background(0, 0, 0)
    push_style()
    fill(0, 0, 0.5)
    circle(width/2, height/2, height-25)
    fill(0, 0, 1)
    circle(width/2, height/2, height-35)
    pop_style()
    
    for c in sorted(circles, key=lambda x: circles[x].radius, reverse=True):
        circles[c].draw_me()
    draw_months(year)
    draw_legend()
    
    save_frame("hols.png")
run()
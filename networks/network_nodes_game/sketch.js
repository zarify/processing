/*
TODO: Make the nodes move again. Should make things more challenging and make
      replay more of a thing, even for the same seed level.
      If I really wanted to be fancy, attaching nodes together would affect their
      movement. I'd need to get the sum of all forces distributed over a graph
      to make that work properly though.
*/
// object containers
var points = {};
var connectors = {};

// global settings
var max_conns = 5;
var sticky_distance = 250;
var speed = 0.5;
var pointsize = 30.0;
var lineweight = 5.0;
var node_size = 10;
var cells = 20;
var max_time = 30;

// animation stuff
var max_move = 0.25;

// internal game settings
var bg_colour = [203, .27, .77];
var bg_timeout = [0, 0.38, .8];
var num_points;
var level_seed = 0;
var time_left = max_time;
var lastClicked = -1;
var game_over = false;

// Timing
var start_time;

// --------- Classes -----------

class NetworkNode {
  constructor(x, y, conns, sticky, id) {
    this.x = x;
    this.y = y;
    this.xvec = random(-max_move, max_move);
    this.yvec = random(-max_move, max_move);
    this.sticky = sticky;
    this.max_conns = conns;
    this.connections = [];
    this.id = id;
    this.stroke_colour = (0, 0, 0);
    this.node_size = 5 + 20 * (sticky / (2 * sticky_distance));
    this.selected = false;
  }

  add_connection(connector) {
    this.connections.push(connector);
  }

  break_connection(connector) {
    let pos = this.connections.indexOf(connector);
    if (pos != -1) {
      this.connections.splice(pos, 1);
    }
  }

  conns() {
    return this.connections.length;
  }

  move_me() {
    this.x += this.xvec;
    this.y += this.yvec;
    if (this.x <= this.node_size || this.x >= (width-this.node_size)) {
      this.xvec *= -1;
    }
    if (this.y <= (this.node_size + 20) || this.y >= (height-this.node_size)) {
      this.yvec *= -1;
    }
  }

  draw_me() {
    push();
    if (this.selected) {
      stroke(0, 0, 1);
      noFill();
      strokeWeight(0.5);
      circle(this.x, this.y, this.sticky);
      strokeWeight(3);
    } else {
      strokeWeight(1);
    }
    stroke(0);
    if (this.max_conns > this.conns()) {
      fill(30, .88, .84);
    } else {
      fill(155, .88, .84);
    }
    circle(this.x, this.y, this.node_size);
    fill(0);
    textAlign(CENTER, CENTER);
    strokeWeight(1);
    text(this.max_conns-this.connections.length, this.x, this.y);
    pop()
  }

  was_clicked(mx, my) {
    let v1 = new p5.Vector(mx, my);
    let v2 = new p5.Vector(this.x, this.y);
    return v1.dist(v2) <= this.node_size/2;
  }

  click() {
    this.selected = !this.selected;
  }

  can_connect(n) {
    let d = new p5.Vector(this.x, this.y).dist(new p5.Vector(n.x, n.y));
    return this.conns() < this.max_conns && n.conns() < n.max_conns && d < this.sticky/2 && this.connections.indexOf(n) == -1;
  }
}

class Connector {
  constructor(n) {
    this.endpoints = n;
    let ids = [parseInt(n[0].id), parseInt(n[1].id)].sort(function(a, b){return a - b});
    this.id = ids[0] + "_" + ids[1];
  }

  draw_me() {
    let end1 = [this.endpoints[0].x, this.endpoints[0].y];
    let end2 = [this.endpoints[1].x, this.endpoints[1].y];
    let p = 1.0 - this.get_length() / ((this.endpoints[0].sticky + this.endpoints[1].sticky)/2.0);
    push()
    stroke(0, 1, 1-p);
    strokeWeight(lineweight * p);
    line(end1[0], end1[1], end2[0], end2[1]);
    pop()
  }

  get_ends() {
    return [this.endpoints[0].x, this.endpoints[0].y, this.endpoints[1].x, this.endpoints[1].y];
  }

  get_length() {
    let end1 = new p5.Vector(this.endpoints[0].x, this.endpoints[0].y);
    let end2 = new p5.Vector(this.endpoints[1].x, this.endpoints[1].y);
    return end1.dist(end2);
  }

  disconnect() {
    this.endpoints[0].break_connection(this);
    this.endpoints[1].break_connection(this);
  }

  check_for_break() {
    let stickies = [this.endpoints[0].sticky, this.endpoints[1].sticky];
    stickies.sort(function(a, b){return a - b});
    return this.get_length() > stickies[0];
  }
}

function intersect(x1, y1, x2, y2, x3, y3, x4, y4, drawIntersect=false) {
  // short circuit if any lines share an end point, since it
  // technically intersects, but actually doesn't for our purposes
  if ((x1 == x3 && y1 == y3) || (x1 == x4 && y1 == y4) || (x2 == x3 && y2 == y3) || (x2 == x4 && y2 == y4)) {
    return false;
  }
  let x12 = x1 - x2;
  let x34 = x3 - x4;
  let y12 = y1 - y2;
  let y34 = y3 - y4;
  let c = x12 * y34 - y12 * x34;
  let a = x1 * y2 - y1 * x2;
  let b = x3 * y4 - y3 * x4;
  if (c != 0) {
    let xi = (a * x34 - b * x12) / c;
    let yi = (a * y34 - b * y12) / c;
    // check for projected intersections
    if ((xi < x1 && xi < x2) || (xi > x1 && xi > x2) || (yi < y1 && yi < y2) || (yi > y1 && yi > y2)) {
      return false;
    }
    if ((xi < x3 && xi < x4) || (xi > x3 && xi > x4) || (yi < y3 && yi < y4) || (yi > y3 && yi > y4)) {
      return false;
    }
    // draw an intersection circle
    if (drawIntersect) {
      push();
      noStroke();
      fill(0, 1, 1);
      circle(xi, yi, 5);
      pop();
    }
    return true;
  } else {
    return false;
  }
}

function get_score() {
  let current = 0;
  let possible = 0
  for (p in points) {
    current += points[p].connections.length;
    possible += points[p].max_conns;
  }
  return [current, possible];
}

function store_score(score, seed) {
  let highscore = localStorage.getItem(seed);
  if (highscore == null || parseInt(highscore) > score) {
    localStorage.setItem(seed, score);
  }
}

function get_highscore(seed) {
  return localStorage.getItem(seed);
}

// Start a new game
function setup_board() {
  level_seed = Math.trunc(random(10000));
  randomSeed(level_seed);
  let dtime = new Date();
  start_time = dtime.getTime()

  // populate points
  let xcellsize = width/cells;
  let ycellsize = height/cells;
  let coords = [];
  for (let x=0; x<cells; x++) {
    for (let y=1; y<cells-1; y++) {
      coords.push([x * xcellsize + xcellsize/2, y * ycellsize + ycellsize/2]);
    }
  }
  
  let i = 0;
  let np = num_points;
  while (np > 0 && coords.length > 0) {
    let pos = Math.trunc(random(coords.length));
    let x = coords[pos][0];
    let y = coords[pos][1];
    coords.splice(pos,1);
    let s = sticky_distance + random(sticky_distance);
    let cons = Math.trunc(random(max_conns))+1;

    points[i] = new NetworkNode(x, y, cons, s, i);

    np -= 1;
    i += 1;
  }
}

function setup() {
  // put setup code here
  createCanvas(800, 800);
  colorMode(HSB, 360, 1, 1, 1);
  background(...bg_colour);
  frameRate(30);

  num_points = 10 + Math.trunc(random(50));

  setup_board();
}

function draw() {
  // put drawing code here
  if (game_over == true) {
    background(...bg_timeout);
  } else {
    background(...bg_colour);
    for (p in points) {
      points[p].move_me();
    }
  }

  let breaks = new Set();
  for (i in connectors) {
    if (connectors[i].check_for_break()) {
      breaks.add(i);
    }
    for (j in connectors) {
      let ends = connectors[i].get_ends().concat(connectors[j].get_ends())
      if (intersect(...ends)) {
        breaks.add(i);
        breaks.add(j);
      }
    }
  }
  // now clean up any breaks from the connectors list
  let b = Array.from(breaks).sort(function(a, b){return a - b});
  b.reverse();
  for (i in b) {
      connectors[b[i]].disconnect();
      delete connectors[b[i]];
  }

  // set up the lines array

  // draw the radius and connection line if a node is selected
  if (lastClicked != -1) {
    push();
    stroke(0, 0, 1);
    strokeWeight(0.5);
    let p1 = new p5.Vector(mouseX - points[lastClicked].x, mouseY - points[lastClicked].y);
    let d = p1.mag();
    let mx;
    let my;
    if (d <= points[lastClicked].sticky/2) {
      mx = mouseX;
      my = mouseY;
    } else {
      let hv = p1.heading();
      mx = Math.cos(hv) * points[lastClicked].sticky/2 + points[lastClicked].x;
      my = Math.sin(hv) * points[lastClicked].sticky/2 + points[lastClicked].y;
    }
    line(points[lastClicked].x, points[lastClicked].y, mx, my);
    pop();
    for (c in connectors) {
      let ends = connectors[c].get_ends().concat([mx, my, points[lastClicked].x, points[lastClicked].y])
      intersect(...ends, drawIntersect=true);
    }
  }

  // draw the lines and nodes
  for (i in connectors) {
    connectors[i].draw_me();
  }
  for (i in points) {
    points[i].draw_me();
  }

  // draw the current score, seed, and time
  push();
  fill(0);
  textSize(20);
  let score = get_score();
  textAlign(LEFT);
  text(score[0] + " of " + score[1], 10, 20);
  textAlign(CENTER);
  text("Seed "+level_seed, width/2, 20);

  if (game_over == false) {
    let dt = new Date().getTime();
    time_left = max_time - ((dt/1000)-(start_time/1000));
    if (time_left < 0.01) {
      game_over = true;
      time_left = 0
      for (i in points) {
        points[i].selected = false;
      }
      lastClicked = -1;
    }
  }

  if (game_over == true) {
    // try and store the current score
    store_score(get_score()[0], level_seed);
    // draw a rect in the middle of the screen for signage
    fill(0, 0, 1);
    stroke(0);
    strokeWeight(3);
    rect(100, 100, width-200, height-200);
    // show your score
    let highscore = get_highscore(level_seed);
    if (highscore == null) {
      highscore = get_score()[0];
    }
    strokeWeight(1);
    fill(200, 0.5, 0.5);
    textSize(30);
    textAlign(CENTER);
    text("Your score: "+get_score()[0], width/2, 250);
    text("Best score: "+highscore, width/2, 300);
    // show high score
    fill(0, .96, .46);
  } else {
    fill(0);
  }
  strokeWeight(1);
  textSize(20);
  textAlign(RIGHT);
  text(Math.round(time_left)+" seconds", width-10, 20);
  pop();
}

function mouseClicked() {
  if (game_over == true) {
    return
  }

  let clicked = -1;
  for (p in points) {
    if (points[p].was_clicked(mouseX, mouseY)) {
      clicked = p;
      break;
    }
  }

  if (clicked == -1 && lastClicked != -1) {
    points[lastClicked].click();
    lastClicked = -1;
  } else if (clicked != -1 && clicked == lastClicked) {
    // deselect the current node
    points[clicked].click();
    lastClicked = -1;
  } else if (clicked != -1 && lastClicked == -1) {
    // selected a new node
    points[clicked].click();
    lastClicked = clicked;
  } else if (clicked != -1) {
    // trying to join a selected node to a new one
    let ids = [lastClicked, clicked].sort(function(a, b){return a - b});
    let cid = ids[0]+"_"+ids[1];
    if (connectors.hasOwnProperty(cid)) {
      connectors[cid].disconnect();
      delete connectors[cid];
      points[lastClicked].selected = false;
      points[clicked].selected = false;
      lastClicked = -1;
    } else if (points[lastClicked].can_connect(points[clicked])) {
      let c = new Connector([points[lastClicked], points[clicked]]);
      let breaks = new Set();
      let ends = c.get_ends();
      for (i in connectors) {
        let l_ends = connectors[i].get_ends().concat(ends);
        if (intersect(...l_ends)) {
          breaks.add(i);
        }
      }
      let b = Array.from(breaks).sort(function(a, b){return a - b});
      b.reverse();
      for (i in b) {
        connectors[b[i]].disconnect();
        delete connectors[b[i]];
      }
      connectors[c.id] = c;
      points[lastClicked].add_connection(c);
      points[clicked].add_connection(c);

      points[lastClicked].click();
      lastClicked = -1;
    } else {
      // leaving this in case I want to play an animation when you click
      // on space rather than a node
    }
  }
}
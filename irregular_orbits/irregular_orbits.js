// change this to using polar coordinates so angles and radius can change for
// each of the orbiters

var node;
var bg_hue;
var camX = 0;
var camY = 0;
var camZ = 0;
var looping = true;

const maxSpheres = 5;
const sphereAlpha = 1;
const maxPathLength = 100;
const sphereDecay = 0.02;

class Nodes {
  constructor(x, y, z) {
    this.x = x;
    this.y = y;
    this.z = z;
    this.a = [0, 0, 0];
    this.ao = [radians(random(-0.5,0.5)), radians(random(-0.1,0.1)), radians(random(-0.1,0.1))];
    this.a_idx = 0;
    this.genSpheres();
  }

  genSpheres() {
    this.spheres = []; // relative x, y, z, radius, hue
    for (let i=0;i<maxSpheres;i++) {
      let dx = random(20, 250);
      let dy = random(20, 250);
      let dz = random(20, 250);
      let r = random(5, 15);
      let h = random(360);
      this.spheres.push([dx, dy, dz, r, h]);
    }
  }

  render() {
    translate(this.x, this.y, this.z);
    rotateX(this.a[0]);
    rotateY(this.a[1]);
    rotateZ(this.a[2]);
    for (let s of this.spheres) {
      push();
      let x = s[0];
      let y = s[1];
      let z = s[2];
      let r = s[3];
      let h = s[4];

      strokeWeight(0.1);
      noStroke();
      translate(x, y, z);

      fill(h, 0.9, 0.9, sphereAlpha);
      sphere(r);
      pop();
    }
    for (let i=0;i<this.a.length;i++) {
      this.a[i] = (this.a[i] + this.ao[i]) % TAU;
    }

    for (let i=0;i<this.spheres.length;i++) { // reduce sphere radius, regen if needed
      this.spheres[i][3] -= sphereDecay;
      if (this.spheres[i][3] < 0.1) {
        this.spheres[i][0] = random(20, 250);
        this.spheres[i][1] = random(20, 250);
        this.spheres[i][2] = random(20, 250);
        this.spheres[i][3] = random(5, 15);
        this.spheres[i][4] = random(360);
      }
    }

  }
}

function setup() {
  createCanvas(windowWidth, windowHeight, WEBGL);
  colorMode(HSB, 360, 1, 1, 1);

  camera(0, // camera x
        0, // cam y
        200, // cam z
        windowWidth/2, // focus x
        windowHeight/2, // focus y
        0, // focus z
        0, 0, 1)

  node = new Nodes(windowWidth*1.3, windowHeight/2, 0);
  bg_hue = random(random(360));
  background(bg_hue, 0.2, 0.8);
}

function draw() {
  //background(bg_hue, 0.2, 0.8);
  ambientLight(0, 0, 0.6);
  pointLight(0, 0, 0.8, windowWidth/2, windowHeight/2, 500);

  node.render();
  
  // move through space
  //node.x += 0.1;
  camX += 1;
  camera(0, // camera x
      0, // cam y
      200 + camZ, // cam z
      windowWidth/2 + camX, // focus x
      windowHeight/2 + camY, // focus y
      0, // focus z
      0, 0, 1)
  
}

function mouseClicked() {
  if (looping) { noLoop(); looping = false; } else { loop(); looping = true; }
}

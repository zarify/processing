# Genuary 2021
This is the set of my attempts at [Genuary 2021](https://genuary2021.github.io/).
I got further than I thought I was going to, given that it was one prompt a day, and at least one of my kids is still very needy, and I wasn't that happy with how a few of them turned out, but the whole process was thoroughly enjoyable, with the [Twitter generative community](https://twitter.com/search?q=%23genuary2021) sharing some awesome work (quite a few with accompanying code that I'm going to dig into when I have some time).

Quite a few of these are animated, but I've added screencaps into the sections below.

## Day 1 - Triple Nested Loop
![img](Day_01/day1.png)

## Day 2 - [Rule](https://www.wolframalpha.com/input/?i=rule+30) [30](https://en.wikipedia.org/wiki/Rule_30)
![img](Day_02/Day2.png)
![img](Day_02/Day2_blue_triangles.png)
![img](Day_02/Day2_eyeballs.png)

## Day 3 - Make Something Human
![img](Day_03_Errors/Day_03_capture.png)

## Day 4 - Small areas of symmetry
I actually quite liked this one. It was based on the idea of [Aaron Penne's butterflies and bugs](https://github.com/aaronpenne/generative_art#creatures) work, but I bumbled through it without looking at how he'd created his. The butterfly has a central line of symmetry, but all of the flowers are asymmetrical.

![img](Day_04/Day_04.png)

## Day 5 - Code golf
I hate code golf.

![img](Day_05_golf_2/5.png)

## Day 6 - Triangle Subdivision
I quite enjoyed making this one. Triangles spear each other and burst out, then spawning a new triangle to spear it, and so on.

![img](Day_06/6.png)

## Day 7 - Generate some rules by hand
This one was such a disappointment. I had a bunch of good ideas using crafting materials like googly eyes afterwards but the ship had sailed.

![img](Day_07/7.png)

## Day 8 - Curve only & Day 9 - Interference Patterns
Curvy waves rotate around, creating some nice patterns than video compression just butchers.

![img](Day_08/8.png)

## Day 10 - Tree
One of the few I was really quite happy with (mostly because the logic built on some code I had written the previous year scanning books and looking at word frequency). It'd be an interesting one to do with more context aware Markov Chains.

![img](Day_10_features/10.png)

## Day 11 - Use something other than a computer as an autonomous process (or non-computer random source) & Day 28 - Use Sound
I'd been playing around with a few examples of reading serial data from a Micro:bit the previous year, feeding accelerometer, LDR, and button data back to a Processing script. This one uses a Micro:bit v2 and also monitors ambient volume.

![img](Day_11/11_28.png)

## Day 12 - Use an API
This is when I started to have a look at p5py, a non-Jython based Processing library, allowing me to properly use external libraries and Python 3 niceness. Unfortunately, its 2D rendering is glacial in comparison, and it feels like there's a memory leak somewhere as well.

This reads public holiday data from an Australian Govt API and charts where they fall in the year from state to state.

![img](Day_12/hols0000.png)

I managed to stuff this up the first time around and didn't notice the API I was using only returned the first 100 results if you didn't specify more, meaning I didn't get any data from my own state!

## Day 13 - Do not repeat
Using the Sieve of Eratosthenes to map out primes, and link non-primes to their factors.

![img](Day_13/d130000.png)

## Day 14 - Subdivision
This was a bit gross. I bounced an invisible point around the screen, and where ever it bounced it created a subdividing line. When the space it bounced into became too small, or it ran out of bounces, it filled the current subdivision and teleported to a new location starting again.

![img](Day_14/d14_bounces0000.png)

## Day 15 - Let someone else decide the general rules of the piece
## Day 16 - Circles only
## Day 20 - No loops
I wrote a basic drawing program for my eldest (3yo) daughter using p5js on her iPad, and she obligingly drew me a little picture for these topics.

![img](Day_15_16_20/IMG_0119.PNG)

## Day 17 - Draw a line, pick a new colour, move a bit
The circle in the center pulses and occasionally changes colour. Depending on the colour the bouncing particle(s) exhibit different behaviour, like changing the curvature of their paths, changing the thickness of the trail, changing colour, or spawning new particles.

![img](Day_17/17.png)

## Day 18 - One process grows, another process prunes
I ran out of time making something good and made this instead. Two processes move around a grid, choosing the next location based on the growth state of its flower.

![img](Day_18/18.png)

## Day 19 - Increase the randomness along the Y-axis
This pulls a random Kanye quote and slowly butchers it as the ball bounces down the screen. It was pretty fun and the idea needs developing to turn it into a full on karaoke style word by word mutation program.

![img](Day_19/19.png)

## Day 21 - function f(x) { DRAW(x); f(x*0.25); f(x*0.5); f(x*0.75); }
And this is where I gave up and went back to Processing's Python mode.
This was based on the work of [Markus Linnenbrink](https://markuslinnenbrink.com/drills/) which looks incredible.

![img](Day_21/marbles.png)

## Day 22 - Draw a line. Wrong answers only.
Didn't like this prompt at all. Drew some horrible fixed curves point by point, randomised some ideas in different locations, and that was about it. I actually kind of like the little tunnels, but that's about it.

![img](Day_22/220000.png)

## Day 23 #264653 #2a9d8f #e9c46a #f4a261 #e76f51, no gradients.
Super fun. Batons rotate as they fall, with the fields influencing their rotational and horizontal motion as they move through. When the fields absorb enough energy they explode, violently pushing away any nearby batons.

![img](Day_23/Day_23_kapow/23.png)

## Day 24 - 500 lines
This is around where I ran out of steam, particularly since I had to go back to work.

## Day 25 - Make a grid of permutations of something
Not terribly exciting. Each particle's motion influences the motion of the particle to the right and below. I think it works better as a static image than an animation.

![img](Day_25/d25.png)

## Days 26 through 31
Not attempted. I took some notes with ideas, but just ran out of time.
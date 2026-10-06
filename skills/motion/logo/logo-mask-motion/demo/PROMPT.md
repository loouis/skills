# Logo Mask Motion Demo Prompts

## Minimal prompt

Use $logo-mask-motion to animate the pieces of this outlined logo moving apart and landing back on the artwork exactly, using one mask per piece.

## Recreate the demo

Use $logo-mask-motion to build a standalone demo of the masking model on five generic leaves:

> Five leaves share one base point: a centre leaf in front, two inner leaves behind it and two outer leaves behind those. Every leaf is a whole shape with a line all the way round. The four back leaves start upright behind the centre leaf, swing out on springs to their places, and the gaps between them and the centre leaf open only as they bounce back.

### Direction

Make the masks the demonstration. Show the parts of one mask first (the petal, the window with the centre leaf cut out, the petal inside it flush, and the mask grown by the gap), then the motion.

### Canonical example

- One row of four small tiles: the petal; the mask; the petal inside the mask, flush; the mask grown by 3 above the waist.
- Two players side by side with one transport: A, the cut-out tilts (the gap is uneven and nicks the base); B, the cut-out grows above the waist only (even gap, lines meet at the base). B is the one to use.
- Controls: play, scrub, slow motion, and a "show the left petal's mask" switch that draws the mask over the player.
- Each leaf only shows on its own side of the centre line, so no leaf's pointed base pokes out past the centre leaf.
- A last section, lines under lines: a ring-and-spokes mark (an outer ring, an inner ring, six slanted spokes extended straight past both ends) in three players sharing one transport: Turn (the spokes turn 120° behind still rings), Grow (the outer ring starts on the inner ring and grows out with its line weight held, uncovering the still spokes) and Thread (each spoke slides in along its own line from outside). Switches to show the mask and the hidden extensions.

### Deliverable

- Create demo/index.html as a standalone document with inline CSS and script, no dependencies, no build step.
- Define `window.__demoPose()` to freeze the players at the moment the gaps are opening, with the mask shown, for the preview render.

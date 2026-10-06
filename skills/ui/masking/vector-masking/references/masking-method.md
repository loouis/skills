# Masking moving pieces of a line-drawn mark

You are animating a mark made of lines (an outlined logo, a line illustration) by moving its
pieces: petals fanning out, letters rising, bars sliding out from behind one another. The pieces
overlap in the artwork, and the artwork has been drawn as one flat outline, so where one piece
sits in front of another the back piece's line simply stops. Your job is to make the pieces move
as if they were real cut-out shapes stacked in front of each other, and to land on the finished
artwork exactly. Masks do all of the hiding. Read all of this before you touch the artwork.

## What is fixed

- Strokes never change thickness. Nothing scales, with one exception for rings that have to
  arrive in an open-line mark (see Line marks): a ring may grow about its centre with its line
  weight held.
- Nothing fades, and nothing is painted over anything. No background-coloured patches, borders or
  fills to fake a hidden edge or a gap. If something must be hidden, a mask hides it.
- Lines never overlap or cross each other as lines mid-motion. A line can run under another
  shape (hidden) or butt up to it (flush); it cannot be seen crossing it.
- The end state is the untouched artwork, to the pixel. When everything has landed you should be
  able to swap in the original paths with no visible change.

## The words

- **Piece**: one whole shape of the mark, as a complete outline with its line all the way round,
  including the part the artwork does not draw because something sits in front of it.
- **Front piece**: whatever is in front of a given piece in the finished artwork.
- **Window**: the mask a piece is seen through. White shows, black hides.
- **Cut-out**: the copy of the front piece subtracted from the window.
- **Flush**: the piece's line runs right up to the front piece's line, with nothing between.
- **Gap**: a small space the artwork has between two pieces (if it has one).
- **Landing**: the moment a piece comes back to its resting place and the artwork's gaps appear.

## The model

1. **Every moving piece is a whole shape with its own mask.** One piece, one mask. Never share a
   mask between pieces and never cut a piece into fragments to avoid masking.

2. **The mask is a window with the front piece cut out of it.** The cut-out is the front piece's
   painted silhouette: its enclosed occluding region plus its stroke, out to the outer edge of
   the stroke. For an unfilled outline this region is filled in the mask only. Preserve
   intentional holes and slots. Not its centreline, not its outline path.

3. **The mask stays still while the piece moves.** The piece animates inside it. So the piece
   comes out from behind the front piece flush, with no gap, like a sheet of paper sliding out
   from under another sheet. While a piece is travelling there is never a gap.

4. **The gap opens only on landing.** As the piece starts to bounce back, or as it settles, the
   cut-out boundary grows outward to open the gap, and its growth follows the piece's bounce
   so the gap feels natural. Until then the mask does not move.

5. **Grow the cut-out, do not slide it.** Opening the gap by making the cut-out bigger all round
   (an outward offset of the cut-out silhouette by the gap distance) gives an even gap the whole way
   along. Sliding the copy sideways gives a gap that is wide at the waist and thin at the tip.

6. **Grow only where the artwork has a gap.** Where lines meet in the finished artwork, for
   example where all the pieces join at a base, the cut-out stays flush. No white slots there,
   ever. Fade the growth to nothing over a stretch where only the piece's fill (not its line)
   touches the front piece, so the fade is never seen.

7. **If the front piece moves, its cut-out moves with it.** Parent the copy in the mask to the
   front piece. Masks chain: a back piece's mask holds copies of every piece in front of it.

8. **A piece that has not started moving is not drawn.** The closed state is the front piece and
   nothing else. Do not rely on masks to hide a piece that is simply waiting.

## Building a piece

- Start from the artwork's own paths. Keep every edge the artwork draws exactly as drawn.
- Add the part the artwork does not draw as the true continuation of the shape: edges that are
  tangent to the drawn edges where they meet, carried on along the real geometry of the shape (for
  a petal, the leaf's own edge; for a letter, the letterform). This hidden part shows briefly when
  a piece overshoots its resting place, so a straight chord or a constant-width stroke will look
  like a kink. End it well inside the piece's own root, somewhere that is covered at every angle.
- Where the artwork's outline runs straight across a join (because another piece's stroke sits
  there), replace that straight chord with a curve tangent to both sides. At rest it is hidden
  under the join; in motion it reads as one line.
- Pivot: turn pieces about a point on the artwork's outer boundary (a base notch), not about the
  centre of the shape. Then the bottoms of the pieces pass through that point at every angle and
  nothing pokes out below the mark. The cost is that a piece turned to upright sits a little to one
  side; deal with that in the window (below), not with extra masks.
- The pieces in front should lead, and stay further open than the pieces behind them, so a back
  piece only ever appears from the outer side of the piece in front, never over its tip.

## Building a mask

- **Window**: a piece only shows on its own side of the mark. For a symmetric mark, a left piece's
  window is the left half-plane. This is what hides a piece's far side when it is closed up.
- **Cut-out**: the front piece's painted silhouette, sitting about 1/20 of a stroke width *inside*
  the front piece's line. The back piece then runs on a little way under the front line, so there
  is solid colour under every edge and no seam. Across an open slot in the front piece (where
  there is no line to hide under) do the opposite: push the cut-out slightly outside, so the back
  piece never pokes into the slot.
- **Growing**: sample the front piece's outline as points with outward normals, then push each
  point out along its normal by `gap × reach(point) × open`, where `open` runs 0 to 1 on landing
  and `reach` is 1 where the artwork has a gap and fades to 0 where lines meet. Use height only
  when it actually identifies those regions. Rebuild the cut-out polygon from those points
  every frame. At `open = 1` the cut-out's edge lands exactly on the
  artwork's cut ends, which is how the hand-over is seamless.
- **Chained copies**: the shapes of moving front pieces go into the mask too, each carried by that
  piece's own transform. Include their hidden parts, since the back piece must be hidden behind
  the whole shape.
- **Hidden front pieces**: if a front piece is itself fully out of sight behind its own mask, do
  not let the back pieces' masks follow it. Its hidden part would cut a hole in their lines. Treat
  it as fully away until it is actually showing.
- **Two pieces that meet on a line of symmetry**: cut each one exactly on the line, and let it
  pass the line only inside the other piece's shape (a thin strip clipped to the other piece).
  Plain overlap leaves a sliver sticking out at the join; no overlap at all leaves a hairline seam.

## Line marks: pieces that run under other lines

Some marks are open lines rather than closed shapes: rings with spokes, a monogram whose strokes
pass under other strokes, a spiral threading in and out of a frame. The model is the same, but the
artwork has no gaps (every join is lines meeting), so the whole gap stage is skipped and three
things change. This came out of a second build, a hexagonal mark with six blades between two
rings, whose draw-on version showed a notch at every junction.

- **The piece is the line, extended straight along its own tangent at both ends**, far enough
  that each end sits under a front piece in every pose the piece will take. A straight
  continuation is the true geometry of a line, so if it ever shows during an overshoot it still
  reads as the same line. Size the extensions from the geometry, not by eye: the butt end, with
  its corners half a stroke either side, has to stay inside the front piece's painted band at the
  band's *narrowest* reach (the flat side of a polygon ring, not its corner). A line drawn only to
  its artwork end stops a fraction short of the ring at some angles and pokes through it at
  others; that is the notch.
- **The mask is the front piece's own stroke.** Window: the front ring's path *filled*, to its
  centreline, which hides everything outside the ring, so the outward extension can be any
  length. Cut-out: the same path stroked black, `stroke-width − 2 × underlap` wide, plus
  `fill: black` where the line must never show inside it, such as a ring's hole. For stroked
  front pieces this replaces the sampled offset polygon: a narrower stroke *is* the underlap.
- **Either side can move.** The default is a back piece moving out from behind a still front
  piece. With lines, the strongest reveal is the reverse: the lines stay still and a front piece
  moves over them (a ring growing from the centre, or contracting to it), so each line is
  uncovered flush at both ends and no line end is ever visible. The copy in the mask follows the
  moving ring, as always.

Rings that have to arrive may grow about the centre with the line weight held: scale the geometry
and set `stroke-width = w / s`, and `(w − 2 × underlap) / s` on the copy in every mask. Two similar
rings can start as one line (the small one scaled to the big one's size by the ratio of their
widths) and peel apart; while they coincide the band between them is empty, so the lines behind
can be present from frame zero without any hiding bookkeeping.

When a line end has to be seen, it is a real end of the line, never a mask edge:

- **Threading**: slide the piece along its own track with the line extended far behind it, so the
  trailing end starts outside the window and never shows; only the leading end travels, and it
  finishes under the front piece.
- **Draw-on gated by the junction**: a line drawing on inside its mask must not reach a front
  piece that is not painted yet, or it stops dead at an invisible edge. Start each line only after
  the front piece's own drawing end has passed their junction (the junction's arc position on the
  front path, the easing inverted to get the time, plus a few frames), and have the front piece at
  the far end fully drawn before the line arrives.
- A drawing head or cursor goes in the same mask as the lines, so it dives under the rings instead
  of crossing them.

A small twist as the lines are uncovered (a few degrees, driven by the moving ring's progress so it
reaches zero as the ring lands) reads as the mark settling rather than moving; the extensions make
it safe.

## The closed state

When pieces are closed up together (for example two petals meeting as one bud) they must read as
one continuous line: a single point at the top, and sides that run straight on into the piece in
front with no notch, no corner sticking out and no step. Do not get there by turning each piece to
its resting angle and hoping. Solve the closed pose: turn and shift the piece until the inside
corner of its tip sits on the centre line (so the two outer edges meet in one clean point and
neither piece's far side shows), its outer edge meets the front piece's edge at the same angle
(no kink), and below that join it stays inside the front piece (so nothing pops into view when it
starts to move). Measure these, do not eyeball them.

## Choreography

- Closed → pieces travel out on springs (overshoot is fine) → at the top of the swing the gaps
  start to open on a small spring of their own → pieces settle → ease the last trace of movement
  to exactly zero → hand over to the original artwork.
- The first few frames after pieces start to move are the weakest: lines less than a stroke width
  apart merge into thick shapes. Keep that phase short; it cannot be avoided without a gap, and a
  gap while travelling is wrong.
- Played in reverse, the piece that arrived last should leave with the others, not before them.
  Give reverse its own schedule for that piece if needed, but never let its line cross another
  piece's line on the way.

## Checking

- Never judge from the live player. Export frames (25fps is enough), make contact sheets, and zoom
  in on every join, tip and base.
- Numeric checks: the closed state must be pixel-identical to the front piece drawn alone; the
  last masked frame must differ from the original artwork by sub-pixel anti-aliasing only; a
  representation switch at the same pose must match on either side; adjacent animation frames
  should contain only the intended motion, with no switch-induced jump.
- Look especially for: white slivers at joins, hairlines where two shapes abut, lines ending in
  mid-air against an invisible mask, little points poking out at a base, and holes where a hidden
  piece's mask is cutting something it should not.
- A check that needs no tooling: in the page, clone the SVG, inline the stroke and fill colours on
  the clone (CSS variables do not survive serialisation), render it to a canvas through a Blob URL
  at the last masked frame and at the artwork frame, and count the pixels that differ. A few
  hundred at 800 px, spread along the junctions, is anti-aliasing; thousands in one place is a
  shape. This caught a spring that had not settled at the hand-over, with the ring a pixel out; the
  residual-motion ease fixed it. The code is in tool-notes.md.

## Doing it in different tools

Read [tool-notes.md](tool-notes.md) for SVG, After Effects / Lottie and Figma implementation details.

## Working with the designer

Build switchable variations rather than one answer, label each with what it does, and send
exported frames with the link. When the designer says "flush" they mean no gap at all; "the gap
should only be there when it lands" means exactly that; "it should look like a continuous stroke"
means solve the join, not soften it. If they send a Figma file showing how they mask, read its
layers before building: the model above came from one.

Alongside "show the mask", give them "show hidden parts": the extended pieces drawn unmasked and
dim, so they can see what the masks hide and why the joins are clean. Keep the old build off the
review page, or label it: a frame the designer sends with a fault you believe is fixed may come
from the earlier version, so check which build it is before changing anything. A fault the mask
makes impossible, such as a line end outside the window, is the tell.

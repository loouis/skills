---
name: logo-mask-motion
description: Animates a line-drawn logo or illustration by moving its pieces (petals fanning out of a bud, letters rising, bars sliding out from behind each other) so they come out from behind one another like real cut-out shapes and land on the finished artwork to the pixel, using one mask per piece and nothing else: no fades, no scaling, no painted-over patches. Use this skill whenever the user wants to animate, bloom, unfold, assemble or reveal an outlined logo, mark, monogram or line illustration whose pieces overlap, whenever they talk about masking shapes so one slides out from behind another, or whenever a logo animation has to end on the exact artwork, even if they do not say "mask". Also use it when a logo animation shows seams, slivers, overlapping strokes, gaps that open too early or pieces that pop, since those are the faults it is built to remove.
---

# Logo mask motion

Take a flat, outlined mark apart into pieces, move them as if they were cut-out shapes stacked in front of each other, and land exactly on the artwork. Masks do all the hiding. The method below came out of a real logo build with a designer who masks in Figma, and every rule in it answers a fault that showed up along the way.

## What is fixed

- Strokes never change thickness. Nothing scales.
- Nothing fades, and nothing is painted over anything. No background-coloured patches, borders or fills to fake a hidden edge or a gap. If something must be hidden, a mask hides it.
- Lines never overlap or cross each other as lines mid-motion. A line can run under another shape (hidden) or butt up to it (flush); it cannot be seen crossing it.
- The end state is the untouched artwork, to the pixel. When everything has landed, swapping in the original paths must make no visible change.

## The words

- **Piece**: one whole shape of the mark, as a complete outline with its line all the way round, including the part the artwork does not draw because something sits in front of it.
- **Front piece**: whatever is in front of a given piece in the finished artwork.
- **Window**: the mask a piece is seen through. White shows, black hides.
- **Cut-out**: the copy of the front piece subtracted from the window.
- **Flush**: the piece's line runs right up to the front piece's line, with nothing between.
- **Gap**: a small space the artwork has between two pieces, if it has one.
- **Landing**: the moment a piece comes back to its resting place and the artwork's gaps appear.

## The model

1. **Every moving piece is a whole shape with its own mask.** One piece, one mask. Never share a mask between pieces, and never cut a piece into fragments to avoid masking.
2. **The mask is a window with the front piece cut out of it.** The cut-out is the front piece's painted silhouette: fill plus stroke, out to the outer edge of the stroke. Not its centreline, not its outline path.
3. **The mask stays still while the piece moves.** The piece animates inside it, so it comes out from behind the front piece flush, with no gap, like a sheet of paper sliding out from under another sheet. While a piece is travelling there is never a gap.
4. **The gap opens only on landing.** As the piece starts to bounce back, or as it settles, the cut-out moves outward to open the gap, and it moves with the piece's bounce so the gap feels natural. Until then the mask does not move.
5. **Grow the cut-out, do not slide it.** Opening the gap by making the cut-out bigger all round (an outside stroke on the cut-out copy, the width of the gap) gives an even gap the whole way along. Sliding the copy sideways gives a gap that is wide at the waist and thin at the tip.
6. **Grow only where the artwork has a gap.** Where lines meet in the finished artwork, for example where all the pieces join at a base, the cut-out stays flush. No white slots there, ever. Fade the growth to nothing over a stretch where only the piece's fill (not its line) touches the front piece, so the fade is never seen.
7. **If the front piece moves, its cut-out moves with it.** Parent the copy in the mask to the front piece. Masks chain: a back piece's mask holds copies of every piece in front of it.
8. **A piece that has not started moving is not drawn.** The closed state is the front piece and nothing else. Do not rely on masks to hide a piece that is simply waiting.

## Build order

1. Read the artwork's paths and work out the stacking: which piece is in front of which, where lines merge, where the real gaps are and how wide (measure them; a logo's gap is usually an even offset of the piece in front, about half a stroke width).
2. Make each piece whole (next section). Keep every edge the artwork draws exactly as drawn.
3. Build each piece's mask (the section after). Start with everything flush and no growth.
4. Add the choreography, then the gap opening, then the hand-over to the original artwork.
5. Export frames and check them (the checking section). Fix what you see, then re-export. Judge from frames, never from the live player.
6. Give the designer switchable variations with plain labels, exported frames and a video, and keep the controls that let them try speeds and timings themselves.

## Building a piece

- Start from the artwork's own paths.
- Add the part the artwork does not draw as the true continuation of the shape: edges tangent to the drawn edges where they meet, carried on along the real geometry of the shape (for a petal, the leaf's own edge; for a letter, the letterform). This hidden part shows briefly when a piece overshoots its resting place, so a straight chord or a constant-width stroke looks like a kink. End it well inside the piece's own root, somewhere that is covered at every angle.
- Where the artwork's outline runs straight across a join (because another piece's stroke sits there), replace that straight chord with a curve tangent to both sides. At rest it is hidden under the join; in motion it reads as one line.
- Pivot: turn pieces about a point on the artwork's outer boundary (a base notch), not about the centre of the shape. Then the bottoms of the pieces pass through that point at every angle and nothing pokes out below the mark. The cost is that a piece turned to upright sits a little to one side; deal with that in the window, not with extra masks.
- The pieces at the back should lead, and stay further open than the pieces in front of them, so a back piece only ever appears from the outer side of the piece in front, never over its tip.

## Building a mask

- **Window**: a piece only shows on its own side of the mark. For a symmetric mark, a left piece's window is the left half-plane. This is what hides a piece's far side when it is closed up.
- **Cut-out**: the front piece's painted silhouette, sitting about a twentieth of a stroke width *inside* the front piece's line. The back piece then runs on a little way under the front line, so there is solid colour under every edge and no seam. Across an open slot in the front piece (where there is no line to hide under) do the opposite: push the cut-out slightly outside, so the back piece never pokes into the slot.
- **Growing**: sample the front piece's outline as points with outward normals, then push each point out along its normal by `gap × reach(height) × open`, where `open` runs 0 to 1 on landing and `reach` is 1 where the artwork has a gap and fades to 0 where lines meet. Rebuild the cut-out polygon from those points every frame. At `open = 1` the cut-out's edge lands exactly on the artwork's cut ends, which is what makes the hand-over seamless.
- **Chained copies**: the shapes of moving front pieces go into the mask too, each carried by that piece's own transform, hidden parts included, since the back piece must be hidden behind the whole shape.
- **Hidden front pieces**: if a front piece is itself still out of sight behind its own mask, do not let the back pieces' masks follow it. Its hidden part would cut a hole in their lines. Treat it as fully away until it is actually showing.
- **Two pieces that meet on a line of symmetry**: cut each one exactly on the line, and let it pass the line only inside the other piece's shape (a thin strip clipped to the other piece). Plain overlap leaves a sliver sticking out at the join; no overlap at all leaves a hairline seam.

`references/svg-recipe.md` has the SVG markup and the per-frame maths for all of this.

## The closed state

When pieces are closed up together (two petals meeting as one bud, say) they must read as one continuous line: a single point at the top, and sides that run straight on into the piece in front with no notch, no corner sticking out and no step. Do not get there by turning each piece to its resting angle and hoping. Solve the closed pose: turn and shift the piece until the inside corner of its tip sits on the centre line (so the two outer edges meet in one clean point and neither piece's far side shows), its outer edge meets the front piece's edge at the same angle (no kink), and below that join it stays inside the front piece (so nothing pops into view when it starts to move). Measure these; do not eyeball them.

## Choreography

- Closed → pieces travel out on springs (overshoot is fine) → at the top of the swing the gaps start to open on a small spring of their own → pieces settle → ease the last trace of movement to exactly zero → hand over to the original artwork.
- The first few frames after pieces start to move are the weakest: lines less than a stroke width apart merge into thick shapes. Keep that phase short. It cannot be avoided without a gap, and a gap while travelling is wrong.
- Played in reverse, the piece that arrived last should leave with the others, not before them. Give reverse its own schedule for that piece if needed, but never let its line cross another piece's line on the way.

## Checking

- Export frames (25fps is enough), make contact sheets, and zoom in on every join, tip and base. Never judge from the live player.
- Numeric checks: the closed state must be pixel-identical to the front piece drawn alone; the last masked frame must differ from the original artwork by sub-pixel anti-aliasing only; a frame just before and just after any window or schedule switch must match.
- Look especially for: white slivers at joins, hairlines where two shapes abut, lines ending in mid-air against an invisible mask, little points poking out at a base, and holes where a hidden piece's mask is cutting something it should not.

## Doing it in different tools

- **SVG / web**: one `<mask>` per piece (`maskUnits="userSpaceOnUse"`), a white window path, black cut-out paths, the piece inside a `<g mask>` with its transform on an inner group so the mask stays put. Rebuild the cut-out `d` each frame from the sampled points. Use `clip-path` for the "only inside the other piece" strip. See `references/svg-recipe.md`.
- **After Effects / Lottie**: each piece is a shape layer with an alpha inverted track matte that is a copy of the front piece, parented to the front piece's layer. The gap is a stroke on the matte layer, animated from 0 to the gap width on landing. Lottie keeps all of this.
- **Figma (for a still or a storyboard)**: a mask group of a rectangle with the front shape subtracted (boolean subtract), used as a mask over the piece; the gap is an outside stroke on the subtracted shape.

`demo/index.html` is a small working example of the whole model on five generic leaves: the parts of one mask, then the motion with a mask you can switch on to see.

## Working with the designer

Build switchable variations rather than one answer, label each with what it does, and send exported frames with the link. When the designer says "flush" they mean no gap at all; "the gap should only be there when it lands" means exactly that; "it should look like a continuous stroke" means solve the join, not soften it. If they send a file showing how they mask by hand, read its layers before building: this model came from one.

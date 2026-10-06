---
name: vector-masking
description: Construct accurate masks for overlapping outlined vector logos, icons and illustrations using whole shapes, occluding silhouettes, clean joins and controlled gaps. Use when masking vector pieces, fixing seams or hidden edges, or keeping their occlusion correct as pieces move. Also covers open-line marks such as rings with spokes or strokes that pass under other strokes: each line is extended under its neighbours and revealed, turned or threaded inside a mask cut from the front stroke, so no notch shows where a line meets a ring.
---

# Vector Masking

Build masks that make outlined vector pieces read as whole shapes stacked in depth. Learn which geometry belongs in each mask, how to hide overlaps without painted patches, and how to preserve the source artwork's joins and gaps. The same construction supports pieces that move.

Read [references/masking-method.md](references/masking-method.md) in full before editing geometry. It contains the construction rules, closed-pose solve, chained masks and inspection criteria. Read [references/tool-notes.md](references/tool-notes.md) for the chosen renderer.

## Construct the masks

1. **Inspect the source.** Read the vector paths and layer order, including an existing designer mask setup when supplied. Keep an untouched reference of the artwork. Record stroke widths, intentional holes, gaps, touching joins and piece order. Use the supplied vectors; do not trace a screenshot when actual paths exist.
2. **Reconstruct whole pieces.** Preserve every visible source edge. Continue hidden edges with the shape's own tangent geometry instead of closing them with arbitrary chords. Keep each piece whole and give it its own mask; do not fragment the artwork to avoid masking.
3. **Build each window and cut-out.** Restrict the window to the piece's intended region. Subtract the complete occluding silhouettes of pieces in front, including the outer painted stroke boundary. An unfilled front outline still needs a filled occluding region inside the mask; preserve intentional holes and slots. Include hidden geometry and suppress occluders that are fully hidden themselves.
4. **Solve joins and gaps.** A rear edge must meet the foreground flush or stop at the source's intended gap. Use a small underlap beneath opaque front ink to prevent antialiasing seams; use outward clearance at open slots. Grow cut-outs along their outward normals to form even gaps, tapering that growth to zero at touching joins. Restrict symmetry-line overlap to the region inside the other piece.
5. **Compare with the source.** Render at matching size, device scale and background. Inspect tips, roots, seams and cut ends. The completed mask construction must match the untouched artwork; fix the mask or hidden reconstruction when it does not.

## When the pieces move

Apply these steps when animation is requested. A still masking task does not need a motion schedule.

- Keep each window stationary while its piece moves inside it. Put the content transform on an inner group. A moving front piece's cut-out follows that front piece in the mask's coordinate space.
- For rooted rotations, use a boundary pivot and solve closed-pose tip alignment, tangent continuity and root containment numerically. Hidden continuations must remain covered throughout overshoot.
- Do not draw pieces before their scheduled start. Keep front pieces leading and further open. Check reverse motion separately if the last-arriving piece would otherwise leave too early.
- Keep travel flush. Begin gap growth at the bounce or settling phase, only where the source has gaps, with roots and touching joins remaining flush.
- Ease residual motion to zero and apply exact resting transforms and gap values. Compare the last masked pose with the source, then hand over without a crossfade. For reduced motion, show the final original immediately.

## Open-line marks: lines under lines

Some marks are open lines with no gaps anywhere: rings with spokes, a monogram whose strokes pass under other strokes, a spiral threading through a frame. The construction is the same; the gap steps are skipped and the following apply. The case came from a hexagonal mark with six blades between two rings, where a plain draw-on showed a notch at every junction.

- **Extend each line straight along its own tangent at both ends**, far enough that each end sits under a front piece in every pose it will take. Size the extension from the geometry: the butt end, with its corners half a stroke either side, must stay inside the front piece's painted band at the band's narrowest reach (the flat side of a polygon ring, not a corner). A line that stops at its artwork end falls short of the ring at some angles and pokes through it at others.
- **Cut the mask from the front stroke.** Window: the front ring's path filled to its centreline, which hides everything outside the ring, so the outward extension can be any length. Cut-out: the same path stroked black at `stroke-width − 2 × underlap`, plus a black fill where the line must never show inside it (a ring's hole). A narrower stroke replaces the sampled offset polygon.
- **Either side can move.** With lines, the cleanest reveal is a still line uncovered by a moving front piece, such as a ring growing from the centre or contracting to it: the line appears flush at both ends and no line end is ever visible. The front piece's copy in the mask follows it, as always.
- **A ring that must arrive may grow with its weight held**: scale the geometry about the centre and set `stroke-width = w / s` on the ring and `(w − 2 × underlap) / s` on its copy in every mask. Two similar rings can start as one line, the small one scaled to the big one's size, and peel apart; while they coincide the band between them is empty, so the lines behind can be present from the first frame.
- **When a line end must be seen, it is a real end, never a mask edge.** Threading: slide the piece along its own track with the line extended far behind it, so only the leading end travels and it finishes under the front piece. Draw-on: start each line only after the front piece's own drawing end has passed their junction, and have the far front piece fully drawn before the line arrives; otherwise the line stops dead at an invisible edge. A drawing cursor goes in the same mask as the lines so it dives under the rings.
- A small turn as the lines are uncovered, driven by the moving ring's progress so it reaches zero as the ring lands, reads as the mark settling; the extensions make it safe.

## Fixed constraints for this method

- Keep stroke thickness constant. Do not animate scale or opacity. The one exception is a ring that has to arrive in an open-line mark: it may grow about its centre with a compensated stroke width so the painted weight never changes.
- Hide with masks, never background-coloured patches, artificial borders or cover fills.
- Do not allow visible line crossings. The rear line goes under a front silhouette or meets it flush.
- Grow a cut-out along outward normals; translating it does not create an even gap.
- Keep the gap at zero while travelling. Fade spatial growth to zero only in a region where no visible line exposes that taper.
- Keep symmetry seams contained inside the other shape. Plain overlap creates slivers; no overlap can create hairlines.
- The final source geometry is authoritative. Fix the reconstruction or mask rather than altering the source to match a defective landing.

## Validate animated masking with exported frames

Export at approximately 25 fps, including onset, overshoot, landing, reversal and handover. Inspect contact sheets plus enlarged tips, joins and roots; a smooth live player can hide one-frame defects.

- The closed composite must match the front piece alone.
- The final masked pose must match the untouched source except for sub-pixel antialiasing; compare aligned renders at identical size, device scale and background. Inspect differences rather than accepting a generous aggregate pixel threshold.
- Compare both representations at the same timestamp at any window, schedule or artwork switch. Adjacent frames may differ only by the intended motion.
- Look for white slivers, thick merged strokes, unsupported line ends, base protrusions and holes cut by invisible occluders. Check forward and reverse.
- A check that needs no tooling: in the page, clone the SVG, inline the stroke and fill colours on the clone (CSS variables do not survive serialisation), render it to a canvas through a Blob URL at the last masked frame and at the artwork frame, and count the differing pixels. A few hundred at 800 px, spread along the junctions, is antialiasing; thousands in one place is a shape. Run it on every variation; identical counts show they reach the same landed state. It caught a spring that had not settled at the hand-over, with the ring a pixel out, which the residual-motion ease fixed. See [references/tool-notes.md](references/tool-notes.md).

When reviewing with a designer, label switchable variations by the behavior they change and include exported frames. Interpret “flush” and “gap only on landing” literally. Alongside a mask-inspection switch, offer “show hidden parts”, the extended pieces drawn unmasked and dim, so the construction is visible. Keep earlier builds off the review page or label them: a frame showing a fault the masks make impossible, such as a line end outside the window, came from an old build, so check which build it is before changing anything.

## Example and scope

Open [demo/index.html](demo/index.html) for a dependency-free SVG study using three original geometric panels. It includes a scrubber, reverse playback, mask inspection, two gap variants and a frozen original for handover comparison. [demo/PROMPT.md](demo/PROMPT.md) documents recreation and frame export.

The demo isolates stationary windows, whole moving pieces and landing-only gap growth. Its simple panels do not exercise rooted petal reconstruction, moving-front chains or tapered join gaps; use the detailed method for those cases. The open-line case is demonstrated in this repository by the ring-and-spokes section of the [logo-mask-motion demo](../../../motion/logo/logo-mask-motion/demo/index.html): spokes turning, a ring growing over still spokes, and spokes threading in. Timing and geometry in the study are examples, not defaults for every logo.

See [REFERENCES.md](REFERENCES.md) for renderer documentation. After Effects, Lottie and Figma adaptations require validation in their actual target tools.

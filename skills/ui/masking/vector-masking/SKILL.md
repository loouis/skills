---
name: vector-masking
description: Construct accurate masks for overlapping outlined vector logos, icons and illustrations using whole shapes, occluding silhouettes, clean joins and controlled gaps. Use when masking vector pieces, fixing seams or hidden edges, or keeping their occlusion correct as pieces move.
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

## Fixed constraints for this method

- Keep stroke thickness constant. Do not animate scale or opacity.
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

When reviewing with a designer, label switchable variations by the behavior they change and include exported frames. Interpret “flush” and “gap only on landing” literally.

## Example and scope

Open [demo/index.html](demo/index.html) for a dependency-free SVG study using three original geometric panels. It includes a scrubber, reverse playback, mask inspection, two gap variants and a frozen original for handover comparison. [demo/PROMPT.md](demo/PROMPT.md) documents recreation and frame export.

The demo isolates stationary windows, whole moving pieces and landing-only gap growth. Its simple panels do not exercise rooted petal reconstruction, moving-front chains or tapered join gaps; use the detailed method for those cases. Timing and geometry in the study are examples, not defaults for every logo.

See [REFERENCES.md](REFERENCES.md) for renderer documentation. After Effects, Lottie and Figma adaptations require validation in their actual target tools.

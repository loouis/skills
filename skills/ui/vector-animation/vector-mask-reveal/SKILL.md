---
name: vector-mask-reveal
description: Animate overlapping pieces of outlined vector logos and illustrations with per-piece masks, constant strokes, flush travel and gaps that open only on landing. Use for petals, letters or bars moving apart or assembling when hidden edges, joins and the final artwork must remain exact.
---

# Vector Mask Reveal

Make an outlined mark behave like whole cut-out shapes stacked in depth. Masks hide edges; the pieces move through those masks, then settle into the untouched source artwork.

Read [references/masking-method.md](references/masking-method.md) in full before editing geometry. It contains the construction rules, closed-pose solve, chained masks and inspection criteria. Read [references/tool-notes.md](references/tool-notes.md) for the chosen renderer.

## Workflow

1. **Inspect the source.** Read the vector paths and layer order, including an existing designer mask setup when supplied. Keep an untouched reference of the finished artwork. Record stroke widths, intentional holes, gaps, touching joins, piece order and the intended closed pose. Use the supplied vectors; do not trace a screenshot when actual paths exist.
2. **Reconstruct whole pieces.** Preserve every visible source edge. Continue hidden edges with the shape's own tangent geometry; do not close them with straight chords that will show during overshoot. Give each independently moving piece its own mask. Use a boundary pivot for rooted rotations; solve tip alignment, tangent continuity and root containment numerically for the closed pose.
3. **Build stationary windows.** Restrict each piece to its intended side of the mark, subtracting the complete silhouettes of the pieces in front. Include the painted stroke boundary. Keep transforms on the moving content inside the mask; a moving occluder's copy follows that occluder in the mask's coordinate space. Suppress pieces until their scheduled start, and suppress occluders that are fully hidden themselves.
4. **Separate travel from landing.** Keep the cut-out flush during outward travel. Begin normal expansion at the bounce or settling phase, growing it only where the final artwork has gaps. Preserve flush roots and touching joins. Keep front pieces leading and further open; inspect a separate reverse schedule if simple time reversal makes a trailing piece leave too early.
5. **Finish exactly.** Ease residual motion to zero, apply the exact resting transforms and gap values, then switch to the original artwork without a crossfade. Compare the last masked pose against the untouched reference before allowing that handover. For reduced motion, show the final original immediately.

## Fixed constraints for this method

- Keep stroke thickness constant. Do not animate scale or opacity.
- Hide with masks, never background-coloured patches, artificial borders or cover fills.
- Do not allow visible line crossings. The rear line goes under a front silhouette or meets it flush.
- Grow a cut-out along outward normals; translating it does not create an even gap.
- Keep the gap at zero while travelling. Fade spatial growth to zero only in a region where no visible line exposes that taper.
- Keep symmetry seams contained inside the other shape. Plain overlap creates slivers; no overlap can create hairlines.
- The final source geometry is authoritative. Fix the reconstruction or mask rather than altering the source to match a defective landing.

## Validate with exported frames

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

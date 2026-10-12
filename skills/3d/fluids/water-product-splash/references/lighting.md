# Make clear water readable

Neutral water gets its colours from the product and studio. Build actual bright fields, dark intervals and a backdrop around the curved boundary. Preserve both transparent windows and broad silver reflections; a bright rim alone can make the sheet read as glass or foil.

A matched test with unchanged water, material and camera showed that additional front cards barely recovered the weak central reflection. Actual reflected directions pointed behind and below the sheet; diffusion there improved the bands. That finding applies to those normals, not every splash.

For a unit incoming view ray `d` and a unit surface normal `n`, the mirror direction is `d - 2 dot(d,n) n`. Sample the actual saved scene at the marked water pixel. Check the hit object's identity: a general raycast may hit a camera-hidden studio card. A reflection direction locates a candidate source; it does not solve all transmitted paths through a thick, folded surface.

Use finite feathered cards to avoid hard rectangular bars. Source size and gradient shape alter the reflected field. Recheck the product as well as the water when moving a card: its colour/finish may change too. Keep geometry and camera fixed for a lighting-only control; record combined changes as combined changes.

The tested baseline is white Glass BSDF with Beckmann distribution, IOR 1.333 and roughness 0. Colour, contrast and apparent thickness still depend on surface shape and surroundings. Use physically meaningful closed boundaries rather than painting coloured streaks onto water. A photograph does not uniquely separate reflection and refraction at every pixel.

Use identical display transforms for raw and denoised comparisons. Display-transformed raw PNGs are not linear EXRs. For new compositing work, combine scene-linear values before the display transform and disclose separate plates.

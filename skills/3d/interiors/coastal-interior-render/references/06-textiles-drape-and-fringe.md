# Textiles: weight, folds, yarn and believable joins

## Work from broad form to fibres

The strongest reference throws cross the arm, pool softly onto the seat, overlap themselves and fall over the front/outer side. Their texture follows those folds. A narrow strip hanging vertically off one side reads like a towel drying. More wrinkles are not automatically more natural.

Build four scales separately:

1. Metre/decimetre scale: supported drape, weight, broad unequal folds and hanging length.
2. Centimetre scale: secondary seat creases, soft overlaps, compressed gathers and edge curl.
3. Millimetre scale: weave cells, raised warp/weft, hem and securing stitches.
4. Submillimetre scale: loose fibres, nap and restrained colour variation.

Fix the broad silhouette first. Fibre count cannot repair stiff cloth. Review the throw in the room before committing to expensive yarn geometry.

## Drape construction

1. Build a cloth sheet with stable surface UVs and adequate resolution for broad folds. Set correct dimensions, gravity and collision thickness; use the actual sofa surfaces as colliders.
2. Arrange support across arm/back and seat so material can flow onto the front and outside. Avoid a perfectly centred regular fold rhythm.
3. Simulate when useful; then inspect evaluated frame bounds, contact and full silhouette. Save the original bake and clearly label later artist shaping. Do not call hand-deformed cloth a new simulation.
4. Keep intentional layered overlap with separated surfaces. Distinguish it from self-intersection, crushed ruffles and coincident sheets. Check the mid-surface, then thickness/yarn projections and visible fold valleys.
5. Add secondary creases around support transitions, not uniform noise everywhere. A tested shape used local seat creases up to 7 mm while preserving a stable gravity envelope; this is a case value, not a required amplitude.
6. Extend a free hanging corner with a continuous falloff. After a sofa lift, move supported cloth with its support and taper changes into the free drape. Snapping individual vertices to nearest upholstery can create jagged folds.
7. Recheck contact after any sofa, cushion, support or cloth change. A prior contact result does not survive a new arm shape automatically.

Before a Blender rest-shape experiment, restore Basis/mesh coordinates, set the rest key value correctly (the failed case needed zero), and inspect frame-one evaluated bounds. A bake that starts displaced or later crushes the cloth is rejected even if it completes. Preserve the stable accepted drape when experimentation regresses it.

## Weave and pattern

Test patterns on the same geometry, camera and lighting: quiet herringbone, fine check, soft stripe and a lightly mottled woven neutral. Keep pattern subordinate to the sofa and stone. Add yarn-scale edge irregularity/interlacing so checks and stripes do not look screen printed onto a plastic sheet.

A developed waffle proposal used a 7.5 mm repeat with up to 1.4 mm physical relief. Separate warp/weft curves and modest short fibres carried the grazing light. These dimensions describe that reference family; a fine linen throw or a chunky knit needs a different scale and structure. Do not force the waffle onto every cloth.

Generate yarn in stable textile coordinates and deform it with the underlying surface. Keep gaps/over-under construction plausible, avoid raised lines that cut through one another and inspect the same patch in light and shadow. Use bump/normal for subpixel detail and actual geometry for visible silhouette or relief. Review denoised versus raw detail: a clean noise-free image can erase the weave.

## Fringe construction: continuity AND fullness

The user preferred full soft bundles. Thin individual strands improved one attachment test but lost the desired appearance. Preserve the preferred silhouette while fixing joins.

Choose a real construction family:

- Warp-continuation fringe: yarns emerge from the woven body, are secured near the edge, then continue into free ends.
- Sewn-on tassels: separate heads/loops and visible fastening to a hem.
- Loop-attached fringe: folded bundles pass through and cinch at an edge.

Do not combine a smooth piping cord, blunt cut ends and unexplained floating tassels. Research sources in [REFERENCES.md](../REFERENCES.md) illustrate different methods; they are not a claim that this custom geometry reproduces a particular commercial textile.

The developed fuller proposal:

1. Four fine header courses integrate the edge with the body instead of hiding it behind thick piping.
2. Each yarn has a continuous lead-in through the weave. Nominal length was 9 mm, with measured minimum around 6.53 mm in the selected study.
3. Gather approximately 18–22 yarns into each bundle over a short soft transition. Avoid a long triangular fan.
4. Add a small securing neck with about two turns, in contact with the gathered yarns.
5. Relax the skirt into shared bends, unequal lengths and slight splay. Keep individual variation within a coherent full group, not rigid comb teeth or isolated sparse hairs.
6. Add small loose fibre ends only after the main yarn shape works.

The implementation used 369 groups and 7,415 continuous paths. Those counts demonstrate scope, not quality or a required budget. Use enough density for the delivered crop; preserve performance through instancing/curves/level of detail where appropriate.

Measure lead-in length along the actual curve, root distance to cloth and segment spacing. A previous screen used >4 mm lead-in, <1.5 mm body proximity and <2 mm maximum lead-in segment. These are local screens, not complete textile validity. A nearby endpoint can pass proximity while looking like a detached flat-cut cap. Inspect the exact join at native scale, all groups around the full hem and the room view. Never fix the join by hiding it under a thicker cord, cropping it out or shrinking the image.

## Contact and clearance checks

Require nonempty cloth/contact samples; missing samples are a failure, not a pass. Use evaluated surfaces and sensible signed distance/intersection checks. Confirm coarse flags on full-resolution triangles. Distinguish intentional separated overlap from crossings. Test solidified cloth, fringe and fibres as appropriate, and state what a sampled test does not cover.

Report rigid sofa/welt-to-table clearance separately from body-only cloth and all-textile bounds. Do not quote 450 mm clear when fringe reduces the conservative local gap to roughly 309 mm. Check full hem against floor/rug and the nearby table, not just cloth body bounds.

Required textile cameras: room, sofa arm/throw, uncovered arm, overhead, seat folds, weave, complete hem/fringe, upholstery detail and low feet/rug support. A cropped glamour detail is insufficient.

## Curtains

Model track/recess and top attachment, plausible heading, thickness/translucency, unequal soft folds and a deliberate floor relationship. Gather clear of operable glazing. Include provision for a privacy/solar layer if the brief calls for it. Do not remove curtains to simplify later material edits.

A modest artist relaxation of around 12 mm broke rigid fold regularity while keeping top attachment and horizontal envelope. This was not a new cloth simulation. Independently check anchors, bounds and floor/door contact before allowing curtains as an exception in a geometry-preservation comparison.

## Rug

Use a continuous weave field at credible scale. A darker rug exposed oversized weave; splitting finer geometry into four patches introduced visible seams. A single global grid removed those seams while preserving footprint, backing and support crown.

The tested fine rug used approximately 6 mm pitch, lower relief, short fibres rising at most 0.65 mm and restrained wool sheen. Dense geometry is optional; the important checks are continuity, scale, contact and appearance. Preserve the rigid support crown under sofa feet and table. Check fibre roots against real yarn geometry, not only an ideal flat backing.

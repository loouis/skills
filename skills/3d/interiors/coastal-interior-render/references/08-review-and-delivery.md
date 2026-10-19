# Geometry gates, honest scoring and delivery

## Fix the rubric before iteration

Whole room: five categories, each /2 — brief/design; architecture/geometry; light/reflections; materials/fine detail; composition/photographic realism. A 9.5 target requires total ≥9.5, no category below 1.8 and no conspicuous geometric/functional defect in any delivered view. This is a subjective art-direction assessment, not certification.

Throw: drape/weight; weave/pattern scale; hem/fringe; fold light/shadow; contact/room integration, each /2. Stool: silhouette/proportion; construction/support; tailoring; material/light response; room integration, each /2. Keep component scores separate from room scores. A 10/10 aspiration does not require declaring perfection.

The developed scene's selected review remained room 9.3, kitchen 9.4, throw 9.5 and stool 9.3. Passing 168 saved-scene checks did not establish reference parity. Earlier high scores were withdrawn when user feedback exposed faults. Keep that honesty in future work.

## Gate sequence

1. **Brief and provenance:** selected product/variant, intended scene, accurate reference claims and asset rights.
2. **Plan:** occupied routes, functional zones, appliance openings and measured rigid/soft projections.
3. **Construction:** supported joints, slab thickness/level, actual pulls, complete sink, connected furniture/feet and continuous balcony rails.
4. **Surface integrity:** UV direction, material assignment, colour/data maps, normals, modifier state, cloth contacts and self-overlap.
5. **Preservation:** unchanged accepted parts, exact scoped edits, all dependencies/cameras/lights. Any intentional exception must pass its own bounds/contact/attachment checks before exclusion.
6. **Saved scene:** reopen the file and run checks there. In-memory success alone does not prove the delivered scene.
7. **Visual review:** all delivered views at appropriate scales, compared directly to references. Technical gates do not calculate visual scores.

Fail closed on absent required objects, cameras, fringe or contact samples. List skipped/unverified checks separately. State whether a test uses bounds, sampled rays, approximate envelopes or full-resolution triangles. Do not describe sampled proximity as exhaustive collision proof or building compliance.

## Review loop

For each candidate:

1. Record the exact baseline and hypothesis: “reduce diffuse appliance-fill spill”, not “make it more premium”.
2. Save a new scene version. Keep the accepted selection intact.
3. Change one family: geometry, material, lighting or camera. Dependent repairs are allowed but record them.
4. Run relevant gates and render a small matched diagnostic set. Preflight all camera names before the first render.
5. Inspect thumbnail hierarchy, room realism, equal-scale reference comparison and native details. Zoom out after microscopic work.
6. Annotate each open defect with box, observation, suspected cause, proposed fix and verification view. Mark resolved items separately; don't colour an item resolved without evidence.
7. Score only the inspected scope. Lower a score if a new view reveals a fault. Reopen affected gates when the user identifies one.
8. Keep or reject based on the evidence. A later version can be worse. Preserve useful negative controls.
9. Once selected, render and review every affected final view before updating the delivery.

Continue while there is concrete useful work toward the requested target. If a dependency is missing or a physical/product detail cannot be verified, state the limitation and progress on independent work. Do not silently stop at a lower score or falsify a threshold to end the loop.

## Camera coverage

Adapt views to the scene; do not require a ritual fixed count. The mature example needed 26 views because the user had found failures in many regions:

- Room: hero, reverse room, walkthrough overview, living detail.
- Kitchen: kitchen detail, drawer fronts, joinery close-up, stone corner, appliance front, complete cooktop, sink overhead, sink working side.
- Seating: counter stool, product detail plus front/side/rear references, sofa upholstery, cushion detail, uncovered arm, sofa feet/support.
- Textile: sofa arm/throw, overhead drape, seat folds, weave/folds, full hem/fringe, fabric close-up.
- Styling/exterior: table objects and exterior depth.

Light changes affect every reflective view; sofa changes affect cloth and support; rug changes affect feet/table contact. Review these dependencies, not only the edited object.

## Review files and annotation

Keep clean render pixels immutable. Write separate PNG/SVG review boards and JSON records. Use normalized box coordinates so the same marked region survives display-size changes. Each record should include scene version/hash, source image/hash, camera, resolution, samples, pipeline, inspected scale, notes, gate results and current status. Include the exact user-flagged region in followup review.

Use readable boxes and numbered notes; avoid covering the defect with a huge label. Wrap titles and inspect the exported annotation, not merely its generation log. The included `review_board.py` preserves the source and records its hash. Its notes file is a format example, not pre-filled evidence for a new render.

Create contact sheets to cover many cameras, but inspect critical originals individually. Keep reference/current/baseline comparisons at equal scale. Label historical or rejected versions clearly and verify that a gallery is showing the selected files rather than stale cached images.

## Render execution and evidence

Use an absolute Blender executable and absolute script path, with `--python-exit-code 1`. Run one GPU render job at a time. Record Blender version/device and render settings. A Python failure may otherwise leave a zero process exit; require per-image completion markers, expected files, nonzero dimensions and the final completion/quit.

The included renderer preflights camera names, renders into a new directory and writes an output manifest. It does not validate scene geometry or choose aesthetic settings. Preserve the scene's aspect ratio unless deliberately changing it. Use CPU for a portable small smoke test; explicitly choose and verify a GPU backend for production. Do not silently describe fallback CPU as a GPU pass.

A tested delivery tier was 2240×1260 at 256 samples for critical views, 1600×900 at 128 for secondary views. These are historical workloads, not quality thresholds. Increase samples/resolution only when actual noise/detail requires it; resolution cannot invent geometry or texture.

## Handoff

Deliver the selected editable scene, clean images, separate annotations, review ledger, asset provenance/licences and a concise recreation recipe. Pack/verify dependencies, record output hashes and preserve previous selections. If a browser gallery is supplied, check its actual links and visual rendering at desktop/mobile sizes. State exactly what was tested; file/link checks alone are not a browser visual pass.

Update project status with selected version, changes, validation, limitations and next useful work. Keep targets open if unmet. Do not inherit scores from a predecessor, an AI concept, a proxy demo or a technically passing scene.

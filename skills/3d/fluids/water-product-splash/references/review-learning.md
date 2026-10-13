# Review each pass and write what it teaches

Before a pass, identify the visible defect and the change intended to test it. Keep unrelated variables fixed when a causal claim matters. For a local correction, start with a cropped border render at native pixel density and modest samples with denoising. Inspect its clean/raw pixels before another change. Review the whole image at agreed milestones and at final quality, including centre, plume, rims, trail and product interaction.

Use separate overlay boxes with numbered notes. Keep the clean image untouched. Each note names the visible feature, why it falls short and the next useful control. Match reference and render framing; do not upscale a crop and describe it as new detail.

Rate five criteria from 0–10: clear transmission; controlled contours/highlights; shape hierarchy; reference-feature compatibility; native cleanliness. Keep the same rubric across passes and retain regressions. The mean is an assistant/reviewer assessment, not user approval. Scores below the requested threshold motivate another supported experiment, not arithmetic inflation. Technical checks and resolution increases add no beauty points. Pre-render failures and diagnostic controls need findings, not fabricated beauty scores.

Record the source/settings revision, renderer, dimensions, image/raw hashes, criterion ratings, remaining defects and next change. A still rating does not transfer to another product or a film. For motion inspect all frames, native details and normal/slow playback; score optics, dynamics and whole-shot appearance separately. Check every rupture and detached drop, especially at cuts/loops.

## Update the skill during the work

After a meaningful result, add a concise entry to the relevant maintained reference:

1. **Observation:** the visible failure or newly working feature.
2. **Test:** what changed and what stayed fixed.
3. **Result:** what the actual full/native/raw review established.
4. **Reusable decision:** what to try, preserve or avoid next time.
5. **Scope and uncertainty:** still/motion, product/view dependence, combined-variable limitations and unresolved defects.

Store the detailed pass record beside the receiving project assets. Keep the portable skill focused on decisions another shot can reuse. Merge a new lesson into the relevant section rather than accumulating a chronological transcript. Promote new defaults only after supported improvement; keep former recipes reproducible and mark superseded readiness clearly.

Public packages should contain generic explanations, reusable code and newly generated examples. Keep supplied references, client names, product geometry/artwork, scenes/caches and private paths in the source project. Revalidate changed code, local links and public content; update the library and maintained installed copy deliberately. Learning is part of the current rendering task, not an unattended schedule.


## Keep section review feasible in memory

Use one heavy Blender process at a time. Disable Persistent Data, restart between expensive stages and reuse frozen mesh geometry for light/material/bounce changes. Do not rebake fluid for shading. If a simulation is required, bake in a separate session, exit it, and render the cache in a fresh process. Lower preview samples reduce tracing work; render borders reduce output/pixel work, but neither guarantees a small geometry/BVH footprint. Inspect mesh density before increasing it, and accept a reduction only after native contour, tiny-feature and optical comparisons.

An expensive authored reconstruction can be frozen once as a water-only checkpoint for repeated crop experiments. Record why it is needed, an output budget, source pins, object/geometry hashes and dependencies; avoid duplicating the product/studio/images per pass. Verify a fresh load and compare matching pixels before treating the snapshot as equivalent. Reconstructed Boolean geometry can fail an exact digest even under the same recipe; record the discrepancy and investigate rather than silently declaring exactness.

Use an explicit local score for each marked defect. A high whole-image average does not clear a weak rim, connection or plume. Follow the user's milestone for a full-quality frame; a10/10 gate requires an honest scoped visual judgment, not automatic promotion or an absolute claim of perfection. Full-frame review can reopen a previously accepted section. It can also expose a different feature outside the original boxes: three local fixes held at final quality while an unreviewed exit still formed an overly deliberate arrow and bead progression. Add a new box and keep the whole score below target until that feature is reviewed; do not transfer the local scores to the entire image. Record interrupted jobs without invented images or beauty scores.


### Separate subdivision construction from tracing

In a dense frozen-water study, a small96sample crop with live subdivision1 exceeded a28GB process-RSS stop. Disabling subdivision completed at5.15GB but exposed a flat cut face, so the lower density was rejected as final. Resolving the inherited subdivision once in an isolated geometry process cost41.92GB peak, then produced an evaluated water-only snapshot. A fresh reload needed0.70GB and the smooth crop completed at5.94GB observed processRSS. This demonstrates a large repeated subdivision-construction cost in that setup, not a universal memory ratio or attribution of all system demand. Keep setup and render measurements separate; processRSS is not total unified, compressed or swap demand. Preserve the original raw mesh, hash the evaluated derivative and validate the native appearance after reloading. Do not run subdivision construction beside a render.

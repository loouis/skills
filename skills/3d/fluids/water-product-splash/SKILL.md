---
name: water-product-splash
description: Reconstruct and refine suspended product-water splashes in Blender, including folded sheets, torn rims, jets, ligaments, droplets and optical distortion. Use for water wrapping around or breaking away from a product, reference-led splash studies, and adapting a reviewed splash to another product. Still reconstruction is tested; validate new collisions and motion separately.
---

# Water · Product Splash

Build water in air with a readable hierarchy: broad transparent folds, accumulated torn margins, tapering ligaments and detached drops. Develop the skill while doing the work: record a demonstrated lesson after each useful experiment, including failures, without turning an untested hypothesis into a preset.

## Choose the relevant work

- **Reconstruct a reference:** read [construction](references/construction.md). Separate what the pixels show from what is known about the source. A still does not reveal the exact rig, impact or trajectories.
- **Improve reflections or transparency:** read [lighting](references/lighting.md). Use the actual surface normals to locate useful reflected sources; adding a front softbox is not a universal fix.
- **Fix a weak pass:** read [diagnosis](references/diagnosis.md). Keep shape, optical field, native density and sample noise as separate possible causes.
- **Adapt to a tap or another product:** read [product adaptation](references/product-adaptation.md), then preserve its selected model, finish and print. Record any requested camera/composition changes explicitly. Fit the splash around its silhouette and readable features; inspect penetration and optical distortion. Recompute lighting for this view. Do not treat the supplied bottle-like proxy as collision geometry for the new product.
- **Score, annotate and keep learning:** use [review and learning](references/review-learning.md). Keep manual beauty ratings, technical checks and user selections separate.

This skill covers suspended splashes. Calm reflecting pools, submerged air cavities and water playing beneath display glass are different problems. Do not replace their established recipes with this one.

## Start from a useful envelope

An authored initial sheet followed by a short FLIP relaxation is a tested way to retain the composition while resolving organic margins. It is one method, not a recovered account of a reference image. [assets/recipe.json](assets/recipe.json) records the tested native settings, bounded mesh filter and source velocities in metres. These depend on the original envelope and scale; do not interpret them as universal water constants.

`scripts/splash_tools.py` provides optional Blender helpers for configuring liquid sources, freezing a cached frame, and applying the bounded filter. It accepts explicit scene/output paths and refuses overwrites. Configuration does not run a bake. Read its CLI help and [construction](references/construction.md) before use. The helpers and generic demo are self-contained; no other skill, private scene or add-on is required.

For a small original optical fixture:

```sh
blender -b -t 8 --python-exit-code 1 -P scripts/render_demo.py -- --output /tmp/splash-study-01
```

Run in a fresh output directory outside the skill. The demo makes a new generic folded sheet, a simple coral object, rounded holes and detached drops. It renders same-run raw/denoised evidence and saves/reopens its scene. It demonstrates the material and shape hierarchy, **not** the complete reconstructed splash or a fluid bake. See [validation](references/validation.md).

## Preserve what the tests established

- Use a closed outer water boundary, neutral white Glass BSDF, Beckmann, IOR 1.333 and roughness 0 as the tested optical baseline. The environment and product supply colour. Roughness is not a substitute for large curved folds.
- Keep the broad centre smoother than the margins. Uniform noise, evenly spaced holes, triangular sails and constant-width spiral tubes fail the observed hierarchy.
- A short solve can improve the margins and still fail the composition. Inspect the whole silhouette before investing in render density.
- Bounded mesh filtering can remove fine geometric striations while retaining torn rims. It is explicit still art direction; document its region, displacement and effect on thickness.
- Iterate on marked defects with cropped border renders and denoising; on a memory-constrained workstation, use64–128sample previews and disable Persistent Data. Keep native pixel density inside the crop. Reuse the frozen/cached mesh for shading; do not re-simulate. Run one heavy job at a time, inspect evaluated mesh density and validate any density reduction against contour/optical detail. A crop does not eliminate geometry/BVH memory. Review the whole image at agreed milestones and final quality before delivery. Score the visible result; additional samples, pixels or passing audits earn no automatic beauty points.
- For routine light, camera or sampling variants, reopen a pinned baseline and apply a recorded recipe in memory. Save a new native checkpoint for necessary geometry or reusable handoffs, rather than duplicating the full scene for every rendered pass.
- A frozen simulated frame, added beads and a refined membrane do not establish animation. New movement needs real product collisions or clearly identified prescribed motion, every-frame inspection and separate motion/optics ratings.

## Keep this skill current

After a supported discovery, update the relevant reference during the task. Capture the observation, controlled change, result, reusable decision and remaining uncertainty. Change the recipe only when the evidence supports a new default; retain rejected settings in the receiving project's evidence. Put new code in the skill only when another shot can reuse it, and test changed helpers.

The skill library is the maintained portable source. Keep its name stable as the knowledge grows. Keep private reference images, product artwork, scenes, caches, paths and full experiment ledgers in the receiving project. Rebuild the generic demo only when a changed method affects what it demonstrates. Validate the package and update project status before completion; keep any installed copy synchronized when that copy is being maintained.

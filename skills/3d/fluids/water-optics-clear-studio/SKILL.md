---
name: water-optics-clear-studio
description: Reproduce and refine clear studio water in Blender with droplet, immersed air-cavity, folded-surface and curved product-contact recipes. Use for transparent contours, reflected lettering, calm pools and local ripples; evaluate motion and fluid dynamics separately.
---

# Water Optics · Clear Studio

Make colourless water readable through curved geometry, coherent medium boundaries, and controlled bright/dark surroundings. Preserve the requested product, print and camera while diagnosing its water. This portable package carries optical-bench generators and the later curved-contact field; its public demo contains newly rendered generic specimens.

## Pick the relevant workflow

- **Droplet, air cavity or folded surface:** read [optical settings](references/optical-benches.md), then use `scripts/render_demo.py` with Blender. A water drop in air and an air cavity in water require different medium orientation.
- **Water around a product:** read [contact and reflection](references/product-contact.md). `assets/contact_field.py` and `assets/contact-settings.json` carry the selected local depression, restrained ripple and irregular optical field. Adapt the contact distance to the actual product; do not copy its reference-cylinder dimensions onto a different model.
- **Jagged or squared reflected lettering, open-water bands or a double-product appearance:** use the matched controls in [diagnosis](references/diagnosis.md) before adding samples or replacing typography.
- **Scoring and annotation:** use [review and iteration](references/review.md). Technical checks, reviewer ratings and user approval remain separate.
- **Animation:** use [motion transfer](references/motion.md); a still or three checkpoints do not validate a film. There is no solver or production motion preset in this package.

## Reproduce an optical bench

From the skill folder, run Blender with a fresh output directory outside this package:

```sh
blender -b -t 8 --python-exit-code 1 -P scripts/render_demo.py -- --output /tmp/water-study-01 --specimen droplet
```

`--specimen` accepts `droplet`, `cavity`, `fold` or `all`. The portable default is CPU, 640 square pixels, 256 samples maximum and a 45-second sampling cap per image. These are demo settings, not the historical final-quality settings. The command creates new scenes, saves and reopens them, renders same-run raw/denoised pairs and writes geometry/settings/hash records. It refuses to overwrite a job directory. Run serially when using a shared rendering machine.

For final optical studies, use 1600 pixels: droplet/cavity had 1536 samples with no cap; fold had 2048 with a 240-second cap. Those original component studies received 9/10 reviewer assessments; that score does not transfer to these CPU demos, another shot, renderer version or motion. See [validation scope](references/validation.md).

## Preserve the optical distinctions

- The specimen material is white Glass BSDF, Beckmann, IOR 1.333, roughness 0. Surroundings supply colour. The product-pool recipe deliberately uses its own varying effective roughness; do not apply that to every droplet.
- Closed surface orientation and the camera's medium matter. Avoid duplicate coincident shells or an unexamined reciprocal IOR.
- Use actual curved surfaces for hero refraction and caustic geometry. Mesh sampling, rendered pixel density, source size and sample noise are different variables.
- Keep calm surroundings and reflected-type distortion as separate review regions. A physically planar surface cannot produce arbitrary wavy reflected lettering. If combining plates, declare it and composite scene-linear values before the display transform.
- Keep visible contact, outer ripples and the first reflected bend together. A mathematically deeper trough can stay hidden behind foreground water at a grazing view.

The latest source treatment received positive user feedback for the small ripples and water appearance after a scoped 9.0/10 assistant assessment. Preserve that direction: a narrow downward front curve, small local ripples, near-contact warp and quiet surrounding water. This is a selected appearance, not a claim of equilibrium wetting or complete motion approval.

Use `water-<specialty>-<look-or-behaviour>` for related skill names. Keep this invocation stable across refinements. Add demonstrated lessons and remaining limits to the relevant reference; keep shot-specific assets and local evidence in the receiving project. Publication does not authorise a deployment, new render campaign or app-wide installation.

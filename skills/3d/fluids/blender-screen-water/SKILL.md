---
name: blender-screen-water
description: Build and render a top-fed Blender FLIP water sheet for tall displays, with clear-water optics, dark depth, feathered reflections and clustered 3D bubbles. Use for cold or hot screen-water effects, native rerenders, partial-loop encoding and drain-and-fade playback. Product geometry and camera choreography are separate.
---

# Blender Screen Water

Create a broad, clear sheet arriving from the top, folding downward across dark depth and catching silver highlights. Cold bubbles travel down with the sheet; Hot uses denser rising bubbles inside the same descending liquid. Keep the water essentially colourless. The bubbles are art-directed air-pocket geometry, not simulated boiling.

## Choose the work

- **Existing files or integration:** inspect the supplied movies, frame sequences and manifests first. Reuse them when sufficient; a file request does not call for a render.
- **New water or changes to flow:** read [references/recipe.md](references/recipe.md), then [references/production.md](references/production.md). The generators contain the exact simulation, lighting and bubble formulas.
- **Higher-resolution output:** reuse a complete supplied cache and prepare a new render job. More output pixels do not create more simulation detail.
- **Loop, exit or behind-glass placement:** read [references/playback.md](references/playback.md). Keep initial arrival, partial repeat and decorative exit separate from controller state.
- **Validation:** follow [references/verification.md](references/verification.md). Inspect matching native crops and multiple repeats; preparation checks do not establish visual quality.

## Prepare a portable job

From this skill folder, with Blender and FFmpeg on PATH:

```sh
python3 scripts/prepare_job.py --rebake --output /tmp/screen-water-job
```

To reuse an explicit simulation directory containing `cache/mesh/fluid_mesh_0001.bobj.gz` through `fluid_mesh_0180.bobj.gz`:

```sh
python3 scripts/prepare_job.py --simulation /path/to/simulation \
  --output /tmp/screen-water-large --scale 2
```

Use `--blender` and `--ffmpeg` for executables outside PATH. The preparer only writes recipe copies, `job.json` and `commands.txt`; it never starts external tools. Use a new output directory. Review the printed probes before full rendering, and run jobs serially unless the target machine has been provisioned for concurrency. The default device is CPU; GPU selection is explicit.

## Preserve the recipe

- Baseline output is **480 × 1800, 30 fps, 180 frames, 6 seconds**. Play arrival once, then repeat **3–6 seconds**. The final 0.6 seconds use a cosine blend; this is not a physically periodic simulation.
- Use the FLIP mesh for the primary sheet. Position deterministic 3D air pockets with raycasts against each frame's surface. Both modes retain descending liquid; only the Hot bubble motion rises.
- Hold water, camera, lighting and exposure constant when comparing modes. Air density alone should not erase dark gaps or turn the water milky.
- Keep native caches, scenes, frames and movies outside the skill. Never overwrite an established revision or combine frames made with different code, helpers, settings or caches. The renderer checks their hashes when resuming and writes frames atomically.
- A saved `waterfall-look.blend` represents frame 90 only. It cannot recover an animation without the external cache.
- Product placement needs a separate consumer scene. Preserve the existing model, glass, UVs and sharp interface. A movie texture under reflective glass still has flat internal water depth; actual volumetric integration requires additional work.

## Included resources

`assets/recipe/` contains the portable Blender builders, renderer, guarded encoder and cache reader. `assets/water-playback.mjs` provides partial-loop mapping, a media adapter and arrival/exit timing helpers; media URLs are supplied by the consumer. `scripts/` prepares jobs, validates behavior and generates the generic material study.

[demo/index.html](demo/index.html) compares newly rendered Cold and Hot bubble materials on an original mathematical folded sheet. It is a shader/bubble study, **not a completed FLIP simulation or motion-quality proof**. The full production recipe remains in the generators. [demo/PROMPT.md](demo/PROMPT.md) documents recreation. No external scenes, reference images, caches, movies or fonts are included.

# Isolated production

## Reuse, rerender or rebake

An existing finished movie is enough for display mock-ups. A complete external mesh cache is enough for a different output resolution or material pass. Changes to the liquid flow or duration need a new bake. Keep these choices separate.

The fixed recipe is 180 frames at 30 fps. `--scale 2` yields 960 × 3600; `--scale 3` yields 1440 × 5400, preserving 4:15. Choose size from the screen's maximum visible pixel coverage. Enlarging output does not improve the cached fluid detail.

Run `scripts/prepare_job.py` with exactly one of `--rebake` or `--simulation`. Missing tools, incomplete caches, invalid sizes and existing destinations fail before writing. All paths are explicit or resolved through PATH. It copies code only; it does not copy the cache or execute Blender/FFmpeg.

The job contains source hashes, dimensions, samples, device and, when reusing a cache, sizes and hashes for all 180 meshes. Local job manifests may contain local input paths; these are working artifacts, not files to publish.

## Execute the prepared commands

`commands.txt` uses background factory-startup Blender processes with `--python-exit-code 1`. The builders reset only that process's scene, so do not execute them inside an unsaved interactive Blender project.

1. Bake the simulation when preparing from scratch. Resolution 256 with mesh scale 2 is substantial work; first review the configured scene with `build_fall.py --output <fresh-directory> --prepare-only` if needed. A prepare-only directory is not a baked cache; use another fresh directory for the real bake.
2. Render Cold probes 1, 30, 90, 162 and 180; Hot probes 30 and 90. Inspect sheet shape, bubbles and native edges before committing to the full render.
3. Render Cold and Hot serially. Frame syntax accepts `1,30,90` or `1:181`, whose end is exclusive.
4. Encode each completed 180-frame sequence into its own fresh media directory.

Default Cycles settings are 128 samples, adaptive minimum 24/threshold .015, denoising, 10 total bounces, 8 transmission and 6 glossy bounces. Output is 8-bit RGB PNG. Review denoised bubble rims and dark folds before raising samples or simulation resolution.

GPU selection is explicit and fails if unavailable. CPU is portable but may be slow. Metal device discovery uses generic kernels before enumeration; a binary-archive environment workaround is included in generated Metal commands. Other backends are exposed for supported installations but are not assumed tested.

## Resume without mixed frames

The renderer records its full recipe hashes, Blender version, dimensions, sampling/device settings and every cache mesh present. Reusing a render directory requires identical settings and inputs. Requested missing meshes fail before scene creation. Completed PNGs are skipped; each new PNG is first rendered to a `.partial.png` and renamed after success. A partial file blocks resuming that revision so an interrupted file cannot silently stand in for a completed frame.

Do not render while the input cache is still being baked or edited. If code, cache or settings change, create a fresh render directory. Preserve failed outputs for inspection rather than deleting established work. Cache format parsing is for BOBJECT meshes from this recipe; unrelated caches may use other coordinates or formats.

## Encode the repeat

The encoder requires all 180 same-sized PNGs and a new destination. It writes an H.264 movie using libx264, CRF 15, slow preset, yuv420p and faststart, then decodes all 180 frames and records hashes. There is no alpha channel or audio.

Frames 1–162 retain the arrival and full-flow portion. Frames 163–180 crossfade toward source frames 73–90 using the exact cosine expression in `assets/recipe/encode_water.py`. At the end, jump forward to time 3.0 / decoded frame 91, not to the arrival. Use the **decoded media frames** for deterministic texture mapping; raw source PNGs do not contain the seam blend. Codec quantization affects decoded pixels throughout, even outside the blend.

Do not simplify the FFmpeg progress expression without checking the seam: its progress parameter runs in the convention expected by the supplied filter. A tiny synthetic-sequence encoding test is included; that proves timing/counts and the blend effect, not the visual quality of real water.

## Portability limits

The primary simulation is a fresh Mantaflow FLIP bake; bit-identical results across Blender versions or hardware are not promised. Render source camera and UV aspect are part of the water asset. Consumer camera movement, product glass geometry and full device interface behavior are separate integration decisions.

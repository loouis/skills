---
name: water-pool-sunlight
description: Make sunlit swimming-pool water in Blender Cycles with the net of sunlight on the pool floor (caustics) and the sun rays coming down through the water, both read from one ray-density map so every shaft stands on a bright patch of floor. Use for any underwater or pool scene that needs floor caustics, light shafts, god rays or dappled water light, as a still or a seamless loop, and whenever a caustic texture reads as a tiled pattern, cracks, marble or wire; evaluate the water surface seen from below and fluid simulation separately.
---

# Water Pool · Sunlight

Light a pool the way the sun does: count where the refracted rays land. A few broad ripple trains bend the sunlight. The density of the rays on the floor is the floor light. The same density, read along the slanted sun, is the sun rays in the water. Nothing is drawn, so nothing repeats and no line has an even width or brightness.

A numpy script makes the map. A Blender module builds the floor, water and ray materials, the two suns and the render settings. There is no fluid simulation, and path-traced caustics stay off.

## Pick the relevant workflow

- **Making or changing the light**: read [the light map](references/method.md) for what the light has to look like, what each number in a spec does, how to put the light where the picture needs it, and the approaches that were tried and failed.
- **Putting it on a scene**: read [the Blender side](references/recipe.md) for the builders, the floor and ray formulas, the water density, and the three things that must be kept from drawing their own pattern on the floor.
- **Moving light**: read [the loop](references/loop.md) for a set of maps that loops without a seam, and how to choose the speeds.
- **Judging a result**: read [checks and limits](references/checks.md) for the order to check in, the patch numbers, the known pitfalls, and what this package was and was not tested for.

## Reproduce the demo

From the skill folder, run Blender with a fresh output directory outside this package:

```sh
blender -b -t 8 --factory-startup --python-exit-code 1 -P scripts/render_demo.py -- --output /tmp/pool-sunlight-01
```

This makes the light map, builds a plain tiled pool from boxes and planes, and renders it at 1280 × 720 with 320 samples on the CPU. On 8 CPU threads the map took about a minute and the render about 13 minutes, on a machine that was busy with other renders. It saves the picture, a JPEG copy, the `.blend`, the maps and a `run.json` with the settings and timings.

- `--draft` is a setup check in a minute or two: a quarter-size map, 640 × 360, 64 samples. Its light looks more cellular than the real thing, so do not judge the look from it.
- `--show floor` and `--show rays` leave one effect out, to see what each adds. Add `--maps <first run>/maps/demo-pool.json` so they reuse the map.
- `--subject` adds a plain ball under water, with a ray-free zone around it and toward the sun so no shaft stains it.
- `--gpu` uses the first GPU device Cycles offers. The demo was checked on the CPU only.

It refuses to write into a folder that already has files. Run serially when using a shared rendering machine. See the [validation scope](references/checks.md#validation-and-limits).

## Use it on a scene of your own

1. **Decide where the sunlight lands and where it stays quiet.** `scripts/screen_to_lookup.py` turns pixels in the picture into the map coordinates a spec needs, and back.
2. **Write the spec.** Copy `assets/demo-pool.json`. Set `depth`, set `domain` to cover everything the camera sees of the floor, and move the groups to the map points from step 1. Turn the train directions if the camera does not look along +y.
3. **Make the map** with `scripts/make_light_map.py` (plain Python with numpy).
4. **Check one train on its own** (`--train`) before trusting the full map. A train whose lines lie across the view is easy to see alone and hard to find in the mix.
5. **Build the scene** with `scripts/pool_sunlight.py`: `floor_light_material`, `tile_material`, `water_surface_material`, `water_body_material`, `sun_ray_material`, `add_suns`, `setup_render`, `setup_sky`. `scripts/render_demo.py` is a small complete example.
6. **Render the floor alone, then the rays alone, then both**, and measure a floor patch with `scripts/patch_stats.py` against the picture before it.

## Preserve the distinctions

- **One map, two effects.** The floor and the sun rays read the same map along the same refracted sun direction. Do not give the rays their own noise: shafts that end on dark floor are what gives a faked version away.
- **Brightness is counted, never drawn.** Every step from ray density to colour is continuous. A threshold anywhere produces hard-edged strokes.
- **Only the map patterns the floor.** The water surface passes shadow rays flat, the floor is lit by a wide sun through light linking, and path-traced caustics are off. Bring any of them back and a second, noisier pattern lands on the tiles.
- **Uneven on purpose.** Each ripple train is too weak to draw lines alone. Lines appear where trains are raised together, so the light gathers in some places and leaves others quiet. An even net of cells everywhere is the failure this method exists to avoid.
- **Crests run away from the camera.** Under water the floor is seen at a low angle, and lines lying across the view collapse into sideways rows.
- **A wash first.** At thumbnail size the picture shows where the sun lands. The fine light is found inside it at full size.
- **Lower the water, not the rays.** When a picture is hazy, thin the water's absorption and scatter for the distance being looked through. Weak rays in thick water read as fog.
- **Keep rays off the subject, off its light and out of the lens.** A ray across a face reads as a painted stripe, a shaft between the sun and the subject leaves a stain on it, and rays against the lens read as fog. Use the clear zones.
- **Whole cycles in a loop.** Each train moves a whole number of wavelengths, so the last frame leads into the first with nothing to hide.

This is a selected appearance, not a claim of physical accuracy. The ray counting is real geometric optics, but the ripples are prescribed and not simulated, the wash and the warm response are look choices, shadows are not refracted, and a loop moves far slower than real ripples.

Use `water-<specialty>-<look-or-behaviour>` for related skill names. Keep this invocation stable across refinements. Add demonstrated lessons and remaining limits to the relevant reference; keep shot-specific assets and local evidence in the receiving project. Publication does not authorise a deployment, new render campaign or app-wide installation.

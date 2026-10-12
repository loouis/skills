# Construct the water at three scales

First box the broad folds, both torn margins, principal jets, trailing sheet, detached drops and product distortion separately. Judge the scale relationship as well as each piece. More small detail cannot rescue a wrong silhouette.

The central membrane needs a few coherent folds with transparent windows. Complexity increases near the margins, where water gathers into rounded rims. Those rims narrow into ligaments with round tips and separated beads. Vary hole size, edge accumulation, spacing and depth; avoid uniform perforation. A lower trail is a narrowing, folded sheet, not a constant-radius helix. Attached condensation is a separate, much smaller scale.

Use closed volumes with consistent outward normals. Inspect solidification around narrow cuts; offset intersections can create spikes. A water drop in air has a different medium boundary from an air cavity immersed in water.

## Shape-led native relaxation

The successful source study used an authored folded envelope as liquid initial volumes, then selected a short native FLIP frame. Compared with ring-launch controls, this kept the intended broad centre, two unequal jets and lower trail while permitting local redistribution and breakup.

The recorded domain is 0.50 × 0.40 × 0.49 m, centred at (0, −0.015, 0.175). Resolution 320, mesh multiplier 2, FLIP 0.90, randomness 0.05, source expansion 0.55 voxels, mesh radius 1.3, smoothing 3/3, 14 frames at 120 fps, time scale 0.7. The still freezes frame 9. These values only reproduce the solver configuration; the authored initial surfaces are equally important. The portable package does not contain the private source surfaces or their cache.

Diffusion was disabled. A surface-tension field of 0.04 was recorded, but its isolated effect and SI calibration were not established. Source expansion helps resolve thin volumes and changes the initial liquid: declare it. This selected branch had no product collider, so it cannot demonstrate wrapping caused by real product impact.

Use `scripts/splash_tools.py configure` on a copy of a source scene. Label each closed source mesh with custom property `splash_source = true` and `splash_role` of `sheet`, `plume` or `trail`. The helper evaluates those meshes before adding flow modifiers, configures the recorded domain, saves the setup and exits. Bake explicitly in Blender after reviewing scale, sources, bounds and any product collider. Budget native density: the final-resolution study used substantial memory; a small fixture check is not a production bake.

```sh
blender -b -t 8 --python-exit-code 1 -P scripts/splash_tools.py -- configure --input sources.blend --output /tmp/splash-config-01
blender -b -t 8 --python-exit-code 1 -P scripts/splash_tools.py -- freeze --input /tmp/splash-config-01/scene.blend --domain "Splash domain" --frame 9 --output /tmp/splash-frame-01
```

The second command requires an actual baked liquid mesh at the selected frame. It rejects an unbaked domain, stores the evaluated mesh, removes its cache modifier and hides the source emitters. Keep the simulation scene/cache separately if another frame may be needed. No renderer version guarantees byte-identical fluid or render output.

## Bounded central refinement

The selected native surface retained fine horizontal combing. A spatially bounded Smooth operation, factor 0.62 over 42 iterations, followed by a maximum 1.8 mm outward offset per side, recovered broader optical bands. The tapered field protected the plume and much of the margin. `assets/recipe.json` preserves that exact world-space field. Both faces moving outward can add up to 3.6 mm total thickness locally; this is not a physical film-thickness measurement.

```sh
blender -b -t 8 --python-exit-code 1 -P scripts/splash_tools.py -- refine --input /tmp/splash-frame-01/scene.blend --object "Frozen splash" --output /tmp/splash-refine-01
```

Adapt the weight region to a new object/camera. Never apply these world coordinates blindly to a scaled or moved tap. Use a copy and inspect actual thickness, closedness, penetrations, silhouette and reflections afterward. This static correction has not been validated over an animation.

During dense edits, defer subdivision. Batch coordinate/normal operations, quantize the field into 128 weight levels, apply smoothing at native density, clear the temporary group and restore subdivision. Reacquire Blender data after destructive modifier operations; retained vertex-group Python references can become stale.

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


## Turn a stiff root fold in depth

In a connected lower-runout study, narrowing and forward bowing improved a broad dark root only modestly. An enclosed hole looked punched out, and a small open-edge cut created ragged teeth. A bounded twist about the local flow axis produced a much clearer turning fold without adding a light or changing the water shader. Extending the turn reduced the abrupt lower transition; native/raw review still governs the final crease treatment.

For an authored static field, use an orthonormal flow/across/depth basis. Let `s` be axial position and `(u,v)` its cross-section, with radius `r`. Rotate `(u,v)` through `theta = angle * max(1-(s/L)^2,0)^3 * max(1-(r/R)^2,0)^3`. In the ideal continuous field, `s` and `r` are retained, so the twist is invertible; restore zero-weight coordinates exactly after floating-point conversion. This avoids the collapsing cross-section of an unrestricted squeeze. Fit the support and axis to the visible incoming flow and outgoing ribbon; do not apply a product-independent world-axis preset. Recheck product clearance, intersections, native reflections and the full shot. This is explicit still shaping, not evidence of liquid dynamics or a motion-ready flow.


## Blend branch deformations across their boundaries

A plume-widening control used hard coordinate partitions and independent height-bin medians. Its edge-length guard caught an18.7mm stretch before rendering. Smoothing the median profiles and blending the branch fields across a finite transition reduced the maximum edge growth to1.06mm in the next control. This passed the geometric guard but still produced an angular elbow and a broad flap at the branch junction. Smooth weights alone do not establish a natural water silhouette.

Keep the preflight failure and reject the resulting visual defect separately. Fit curvature, taper and accumulated water at the junction rather than uniformly widening an entire branch. Move detached droplets rigidly when adjusting their path; stretching the mesh of every drop with the parent field can destroy the useful round/elongated breakup hierarchy. Review parent mass, each daughter curve, necks and separated beads at native density before adopting a shaping field. These are still-image corrections, not evidence of trajectories from a fluid solve.


### Preserve a branch cross-section when changing its direction

A large camera-plane displacement narrowed an upper daughter even with its explicit width parameter left at1: the selection weight varied across the branch, so different vertices received different shifts. Strong extra narrowing produced thin ligaments with heavy paddle tips. Maximum edge-growth and unchanged lower geometry did not catch this aesthetic failure. Inspect section width and the terminal mass, not just displacement bounds.

A tested alternative rotates the outer branch rigidly about the camera axis, uses a full-weight plateau covering its complete cross-section, and blends the change near the root and selection boundary. The plateau preserves distances; the blend is still a deformation and requires its own checks for pinching, overlap, optics and connected flow. Move nearby detached drops rigidly and review actual separation from each new tip. A regular vertical ladder of beads can look authored even when the shape checks pass.

Adding an extra perforated membrane is not automatically more natural. A two-hole triangular envelope produced a sail; a later cut in the finished cache left a deliberate scallop. Putting that tear into the initial source and relaxing it rounded the edge, but retained an overly lateral fin. Rotating the added web then formed a broad folded lip. Correct the dominant flow direction and source hierarchy before adding more lace or surface detail; retain the simpler reviewed volume when an added web is a regression. These are still-composition findings, not motion validation.

# Validation scope

The source reconstruction went through thirteen manually scored beauty passes and three native fluid experiments. Its selected frozen still was assessed at 8.08/10 (displayed 8.1); simpler plume branching, an orderly lower sweep, residual ridges/strands and denoiser softness remained. This is evidence for the procedural lessons, not a score for this public demo, a promise of identical reproduction, or approval of another product/animation.

This portable package retains the exact solver/filter settings, reusable native helper operations and generic explanations. It excludes private source geometry, scenes, artwork, reference images, caches and asset manifests. It therefore does not independently regenerate that complete source reconstruction.

## Package checks

Run the small fixture checks with Blender:

```sh
blender -b -t 8 --python-exit-code 1 -P scripts/test_native.py
```

The fixture checks a fresh-output guard, bounded field/offset, temporary-group cleanup, source velocity, rejection of an unbaked freeze, a tiny three-frame native bake, independent frozen geometry and reopening. This tests real helper behavior at low resolution; it does not establish production dynamics, source-shape parity or a full-resolution bake.

The demo generator renders a new original authored membrane and optical proxy, then reopens the saved scene and checks output dimensions, neutral IOR/roughness, closed-shell modifier, lack of a fluid claim and same-run raw output. Blender 5.2.1 LTS / CPU / eight threads is the tested environment. The demo uses 256 samples maximum and a 60-second cap; it is not a convergence guarantee. Compatibility with other versions/backends remains untested.

Review the full fixture and raw detail manually. Its regular cut geometry and edge accumulation are intentional component-study limits, not examples of fully natural breakup. The demo has no production beauty rating. The generic fixture, native helper checks and browser checks remain separate from historical still assessments.

Current package verification passes all 12 native helper checks, 7 saved-demo checks and 7 browser checks. Desktop and mobile layouts, full native beauty/raw images and the generated browser preview were visually inspected. See [checks.json](checks.json) for the bounded assertions and source hashes. The first helper test exposed Blender treating a zero-strength Smooth modifier as disabled; the helper now skips no-effect operations.

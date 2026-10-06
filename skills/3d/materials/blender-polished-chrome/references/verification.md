# Verification and delivery

## Establish a comparison contract

Record which objects/materials may change, the master-file hash, render settings and a baseline render. For a finish-only edit, preserve original mesh data, transforms, evaluated geometry/normals, camera, exposure, color look and out-of-scope materials. For an authorised lighting revision, also name the intentional world/card/light changes so the comparison is not described as roughness-only.

Hash original files again after the work. Reopen saved revisions to verify disk contents, not only the unsaved in-memory scene. Copy Blender RNA values to plain Python before opening the next file.

Useful comparisons:

- **Source mesh:** vertices, edges/faces, transforms, material indices and smooth flags. Include relevant UV/color attributes, shape keys and modifier state for that asset.
- **Evaluated mesh:** coordinates/topology plus corner normals via the evaluated dependency graph. Release temporary meshes with `to_mesh_clear()`.
- **Camera:** world matrix, type, lens/ortho scale, sensor fit, shift, clipping and projection settings. Preserve aspect ratio and camera rays when rendering borders.
- **Materials:** node types, sockets, links, ramp points/interpolation, image bindings and relevant properties, recursively including node groups. A count of materials or nodes does not prove equality.
- **Lighting:** world graph, panel transforms/materials, lights and ray visibility; floor glossy visibility restored and useful upper diffusion retained.
- **Saved output:** named independent scene, intended sample/quality settings, packed or resolvable dependencies, sensible relative output paths and no missing assets.

Define tolerances only where floating-point serialization requires them. Do not ignore a changed normal or camera because vertex counts happen to match. Equality checks prove preservation of the recorded properties, not visual realism or an exhaustive equivalence of every Blender feature.

## Native render checks

A demanding product-render starting configuration is Cycles, AgX with a selected contrast look held constant, fixed exposure, 1024 sample ceiling, `.004` adaptive threshold, 96 minimum samples, denoising and a 1 px filter. Full focus (DOF and motion blur off) helps inspect detail. Retain a user's established color pipeline instead of changing it just to match these examples.

For large output, roughly 4K full frames and native detail renders around 3200 px wide can be useful. Choose dimensions for the actual delivery. Save a 16-bit PNG master and, if needed, a quality-98 JPEG at the same pixel dimensions. These numbers do not guarantee quality; inspect noise, aliases, texture and edge resolution at 1:1.

To increase detail while preserving perspective, use the same camera and a higher full-frame resolution with matching render-border bounds. Do not enlarge a small raster crop and call it native. Check actual output dimensions because border rounding can add a pixel.

Inspect:

1. Entire frame: composition, contact, backdrop, unintended card shadows and continuous reflections.
2. Upper form: controlled falloff, side ridges, recesses and highlight transitions.
3. Body and base: no finite stripe endings, flat grey patches, fuzzy joints or erased edges.
4. Matching before/after at identical camera and crop bounds. A web reveal should support pointer and keyboard, preserve image alignment, and pair downloads with the displayed version. Cap display width or offer native files so enlargement is explicit.

Record concrete observations and remaining defects. Do not convert passing checks into a numeric photorealism rating or claim a measured finish match without appropriate reference evidence.

## Packaged helper and demo validation

From the skill folder, with Blender on PATH:

```sh
blender -b --factory-startup --python-exit-code 1 -P scripts/test_reflection_card.py
blender -b --factory-startup --python-exit-code 1 -P scripts/render_demo.py -- --output /tmp/metal-demo-v01 --width 1600 --samples 256
```

The demo generator only builds its own generic scene. It refuses an existing output directory, saves independent satin / polish-only / controlled revisions, renders matched PNG/JPEG pairs and reopens each scene to check intended settings and invariant geometry/camera. CPU is the portable default; `--device METAL` (or CUDA/OPTIX/HIP/ONEAPI) selects a supported local device without saving preferences. No private scene or HDR is needed. The published demo uses the three generated JPEGs; its HTML adds only comparison controls and labels.

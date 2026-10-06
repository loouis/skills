# Polished metal study

## Minimal prompt

Use $blender-polished-chrome to refine a Blender product scene into convincing mirror-polished metal. Keep the confirmed metal identity, original geometry, camera and exposure. Diagnose roughness and the reflected environment separately.

## Recreate this demo

Create a generic stepped cylinder and upright ring on a grey floor in Blender Cycles. Use an artistic uncoated stainless steel approximation with linear reflectance [0.56, 0.57, 0.58], metallic 1 and zero coat. Keep geometry, camera, exposure and broad feathered diffusion identical in three revisions: satin roughness 0.120; polish roughness 0.035; and the same polish with a feathered dark floor reflection card. The last variant must keep the floor visible to glossy rays and retain the objects' contact shadows. Render actual geometry, save independent scenes, inspect full frames and native details, and build an accessible before/after reveal with matching version downloads. Do not use external product assets or AI replacement imagery.

## Rebuild the rendered assets

From the skill folder, use Blender on PATH (or substitute your Blender executable):

```sh
blender -b --factory-startup --python-exit-code 1 -P scripts/test_reflection_card.py
blender -b --factory-startup --python-exit-code 1 -P scripts/render_demo.py -- --output /tmp/metal-demo-v01 --width 1600 --samples 256
```

The output directory must not already exist. The portable default is CPU; use `--device METAL`, `CUDA`, `OPTIX`, `HIP` or `ONEAPI` only on a supported host. The script resets its isolated Blender process to an empty scene; do not run it inside an unsaved interactive project. It does not change global preferences.

Inspect all three renders, then copy `satin.jpg`, `polish-only.jpg` and `controlled.jpg` into this demo folder. Keep the generated PNGs and `.blend` files locally if needed; they are not required to browse the demo and are not included in the published package. Open `index.html` directly or serve the skill folder with `python3 -m http.server 4173 --bind 127.0.0.1` and visit `/demo/`.

From the repository root, regenerate the 1280 × 720 browser preview:

```sh
node scripts/build-previews.cjs blender-polished-chrome
node scripts/build-gallery.cjs
node scripts/validate-skills.cjs
```

The preview selects the controlled result. The live page initially compares lower roughness with reflection control. Use the range slider (arrow keys, Home/End) or drag the image. The left baseline and its native download follow the selected variant; the right stays controlled.

## Remix

Apply the same comparison to an original rounded block or curved handle. Preserve the material's actual identity; use a chromium reference if chrome plating is specified. Scale and rotate the floor card to follow the new object's reflected rays instead of copying world coordinates. Adapt camera and lighting during setup, then hold them fixed for the comparison.

## Provenance and validation

All geometry, shader setup and rendered images were created for this generic demo. No downloaded HDR, client assets or external textures are used. Published images were rendered in Blender 5.2.1, Cycles/AgX High Contrast, 1600 × 1200, 256 sample ceiling, .006 adaptive threshold, 64 minimum samples, denoising and a 1 px filter. Rendered JPEGs are quality 98; `preview.jpg` is the repository's browser screenshot.

The generator reopens all three scenes and verifies geometry/evaluated normals, camera, exposure, color look, intended roughness/card state and retained steel reflectance. Those checks establish preservation, not a measured alloy match or universal physical accuracy. The floor card is an art-directed emission/transparent surface and can affect indirect light.

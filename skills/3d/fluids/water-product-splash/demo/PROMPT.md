# Recreate the optical fixture

## Minimal prompt

Use $water-product-splash to make a generic folded water sheet in front of a coral cylinder. Show broad optical bends, rounded holes and detached droplets; save raw and denoised evidence and clearly label it as an authored component fixture.

## Reproduction

From the skill folder, run:

```sh
blender -b -t 8 --python-exit-code 1 -P scripts/render_demo.py -- --output /tmp/splash-demo-01
```

The output directory must not exist. Inspect the new 768 × 480 PNGs at native size. Convert `beauty.png` and `raw-Image.png` to same-size JPEGs at quality 94 as `demo/beauty.jpg` and `demo/raw.jpg`; do not retouch them. Test box/raw/detail controls on desktop and mobile. Capture `demo/preview.jpg` at 1280 × 720 in the default pose. This fixture has no inherited production beauty score and is not a fluid bake.

## Remix prompt

Use $water-product-splash to adapt a suspended splash around my selected product. Preserve its model, finish and camera. Compare broad folds, plume, torn margins and trailing sheet against the reference. Score and annotate each beauty pass. As experiments establish useful findings, update the skill with the method, failures and remaining limits.

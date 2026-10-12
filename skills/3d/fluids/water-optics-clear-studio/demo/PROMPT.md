# Recreate the public study

## Minimal prompt

Use $water-optics-clear-studio to render a droplet, an immersed air cavity and a folded water surface. Keep the water colourless and save raw and denoised output.

## Reproduction

From the skill directory:

```sh
blender -b -t 8 --python-exit-code 1 -P scripts/render_demo.py -- --output /tmp/water-demo-01 --specimen all --size 640 --samples 256 --seconds 45
```

The output directory must be new and outside the skill. Every scene is generated from generic mathematical geometry, saved, reopened and checked before rendering. Inspect the native PNGs and same-render raw files. Convert those PNGs to same-size JPEG previews at quality92; do not retouch them. Put the three beauty JPEGs at `droplet.jpg`, `cavity.jpg`, `fold.jpg` and raw equivalents at `droplet-raw.jpg`, `cavity-raw.jpg`, `fold-raw.jpg` beside `index.html`. Open the page and test both toggles before capturing the1280×720 preview.

## Remix prompt

Use $water-optics-clear-studio to adapt the curved-contact recipe to my existing product. Preserve its geometry, label and camera. Compare curved contact, the first reflected letter and smooth open water in separate boxes. Explain any plate composition, score each rendered pass and validate motion separately if requested.

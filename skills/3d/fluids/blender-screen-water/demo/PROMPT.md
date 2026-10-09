# Screen water material study

## Minimal

Use $blender-screen-water to create clear screen water with dark depth, feathered silver reflections and irregular bubble clusters. Keep the descending sheet separate from the bubble motion.

## Recreate this demo

Create an original, closed mathematical folded sheet in Blender, using no imported scene or texture. Render two identical views with the bundled water/backing/reflection setup: Cold's sparse air pockets and Hot's denser field. Use the exact seed and placement formulas at frame 90, but label the geometry as a material proxy, not a FLIP simulation. Keep camera and exposure fixed. Show the native stills side by side on a pale neutral page with a detail-inspection toggle and an elapsed-time slider explaining arrival-once/partial-repeat mapping. Do not animate the stills as if they prove fluid motion.

## Rebuild the generic renders

From the skill folder, with Blender on PATH:

```sh
blender -b --factory-startup --python-exit-code 1 \
  -P scripts/render_demo.py -- --output /tmp/screen-water-study --samples 64
```

The script makes new generic proxy geometry in a fresh directory, writes one synthetic BOBJECT mesh, renders Cold and Hot at 480 × 1800, and saves JPEG derivatives. It uses CPU by default; `--device` selects a supported GPU. It never bakes a fluid sequence. The proxy is a finite folded slab; its static folds do not establish the production simulation's behavior.

Inspect both outputs before copying `cold.jpg` and `hot.jpg` into `demo/`. Keep generated cache, scenes and PNG masters outside the repository. Published stills were made with Blender 5.2.1, CPU Cycles, a 64-sample ceiling, the recipe's adaptive/denoising settings and AgX Medium High Contrast. The browser detail switch magnifies the JPEG; native downloads are available.

Open `demo/index.html` directly; it needs no network assets or build step. From the repository root:

```sh
node scripts/build-previews.cjs blender-screen-water
node scripts/build-gallery.cjs
node scripts/validate-skills.cjs
```

Set `NODE_PATH` to an existing Puppeteer installation and `PUPPETEER_EXECUTABLE_PATH` to an installed Chrome binary when needed. The preview is 1280 × 720.

## Remix

Use $blender-screen-water to prepare a new FLIP job or rerender a supplied complete cache at 2× native resolution. Keep the same source camera, optics and deterministic bubbles. Review probes, render a complete sequence, encode its forward repeat, and watch at least two repetitions before using it in a separate display scene.

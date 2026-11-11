# Recreate the public study

## Minimal prompt

Use $water-pool-sunlight to render a plain tiled pool seen under water, with sunlight on the floor and sun rays coming down through the water. Show the picture with both, with the floor light alone and with the sun rays alone.

## Reproduction

From the skill directory:

```sh
blender -b -t 8 --factory-startup --python-exit-code 1 -P scripts/render_demo.py -- --output /tmp/pool-sunlight-01
blender -b -t 8 --factory-startup --python-exit-code 1 -P scripts/render_demo.py -- --output /tmp/pool-sunlight-02 --maps /tmp/pool-sunlight-01/maps/demo-pool.json --show floor
blender -b -t 8 --factory-startup --python-exit-code 1 -P scripts/render_demo.py -- --output /tmp/pool-sunlight-03 --maps /tmp/pool-sunlight-01/maps/demo-pool.json --show rays
```

Each output directory must be new and outside the skill. The first run makes the light map; the other two reuse it, so all three pictures show the same light. The pool is generated from plain boxes and planes and saved as a `.blend` beside each render.

Each run writes `pool-sunlight.png` and a same-size `pool-sunlight.jpg` at quality 92. Do not retouch them. Put the three JPEGs beside `index.html` as `both.jpg`, `floor.jpg` and `rays.jpg`. Open the page and test the three buttons before capturing the 1280×720 preview.

## Remix prompt

Use $water-pool-sunlight to light my existing Blender pool scene. Keep its geometry, camera and subject. Put the sunlight on the floor where my reference has it, keep one area quiet, and keep the sun rays off the subject. Make the light map for my pool's depth and my camera's view, check one ripple train on its own before the full render, and report the patch numbers next to the reference numbers. If it has to move, make it loop.

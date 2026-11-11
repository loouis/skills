# Checks and limits

Read this when judging a render, comparing two versions, or deciding whether this package covers a case.

## Check in this order

Look before measuring. Each step catches a fault the later ones hide.

1. **The thumbnail.** Shrink the picture to about 320 pixels wide. It must show where the sun lands and where the floor stays quiet. An evenly bright floor is a wash problem: fix the wide groups and the wash lobes before touching anything fine.
2. **The floor alone** (`--show floor`), at full size, against the five points at the top of [the light map](method.md).
3. **One train alone** (`--train I`, then a floor-only render with `--maps`). Its lines must run away from the camera and converge. Lines lying across the frame mean the direction is wrong for this camera.
4. **The rays alone** (`--show rays`). Separate shafts, strongest just under the surface and thinning on the way down. Not an even haze, none across the subject, none against the lens. The plain floor under them carries soft grey smudges: that is the shade of the shafts, and it is expected (see [the rays also shade](recipe.md#the-rays-also-shade)).
5. **Both.** Follow two or three shafts down by eye: each one stands on a bright patch of floor.
6. **Then the numbers**, against the picture before this one.

## Patch numbers

```sh
python3 scripts/patch_stats.py /tmp/pool-sunlight-02/pool-sunlight.png@330,300,950,560 /tmp/pool-sunlight-02/pool-sunlight.png@960,300,1270,470
```

Give a patch of floor as `x0,y0,x1,y1` in pixels of the picture as it is. The picture is resized to 1000 pixels wide first (`--width`), so pictures of different sizes compare.

| Number | What it says |
|---|---|
| `line_frac` | Share of pixels more than 18 grey levels above their blurred surround: fine bright line. |
| `strong_frac` | The same above 35: the hot centres. This one moves first when the light turns wiry. |
| `soft_lit_frac` | Share that is lit but is not a line: the pale glow. |
| `local_contrast_sd` | How busy the patch is. |
| `soft_sd` | How much the broad wash varies across the patch. |

What the demo pictures give (1280 × 720, 320 samples):

| Picture | Patch | Line | Strong | Contrast |
|---|---|---|---|---|
| Floor only | sunlit, `330,300,950,560` | 1.47% | 0.09% | 4.8 |
| Floor only | quiet side, `960,300,1270,470` | 0.28% | 0.02% | 3.1 |
| Both | sunlit | 0.76% | 0.02% | 4.0 |
| Both | quiet side | 0.08% | 0.01% | 2.5 |

Two things to take from the table. The sunlit patch has about five times the line share of the quiet side, which is the unevenness the method is for. And with the sun rays on, the line share halves: the shafts veil the floor from the lens and shade the bright patches they stand on. So compare floor-only with floor-only, and both with both.

The numbers depend on how large the floor is in the picture. From a camera close to the floor, where the same light fills more pixels, a reference picture measured 4.0% line, 0.62% strong and 8.4 contrast; the result accepted against it measured 3.9%, 0.60% and 7.7; an earlier attempt that read as wire measured 8.5%, 4.5% and 15.5. So the numbers are for comparing one view with itself or with a reference seen the same way, never as targets on their own. A `--draft` picture also measures differently, being smaller and made from a coarser map: the demo's sunlit patch reads 0.17% line there against 0.76%. Do not compare a draft with a full render.

When matching the water colour to a reference picture, compare a grid of boxes across the frame. One box hides a gradient that is wrong.

## Unit check

`--metres` builds the same scene at 0.001 scene units per millimetre. Rendered at 480 × 270 with 64 samples, the millimetre and metre pictures differed by 0.1 grey level in 255 on average, and by 1 level at the 99th percentile, which is render noise. Run this pair again after changing any length or density in `pool_sunlight.py`: a value that was not converted shows as a clearly darker or hazier picture.

## Loop checks

Loop maps 1, 2 and 168 of a 168-frame loop were made at a quarter of the full size (`--frames 1 2` and `--frames 168 168`, with `--bins 1024 --photons 3584`) and rendered at 480 × 270 with 48 samples:

- Frame 1 and frame 169 rendered to the same picture, pixel for pixel. The sequence is cyclic, so 169 reads map 1.
- Frame 1 and frame 2 differed by 1.35 grey levels on average. It moves.
- In the maps, the step across the seam (168 to 1) matched an ordinary step (1 to 2): 213.8 against 213.8 in 16-bit units for the sharp map, 65.0 against 65.2 for the soft map.
- Map 1 of the loop was identical to a still map made at the same size from the same spec.

The other 165 maps of the loop were not made here.

The first and third are the ones to repeat for a loop of your own. A seam shows as a step several times the ordinary one.

## Pitfalls

- **A draft map is more cellular.** A map with a quarter of the cells shows a net of even cells that the full map does not have. Check setups with it, not looks.
- **Think of the blurs in screen pixels.** `blur_mm` and `soft_blur_mm` are sizes on the floor. A distant camera cannot show a 1 mm blur at all, and a very close one starts to show the cells of a coarse map. Work out millimetres per pixel at the floor before changing either.
- **Keep the headroom.** Density is stored divided by `scale` (64). The demo's sharp map peaks at 53 times the mean. A smaller scale clips the knots flat, and the warm centres go with them.
- **Row order.** The script writes the top row of the file as the largest y, which is what Blender expects. A map made another way may need flipping; the sign is light that gathers at the mirror image of where the spec put it, away from the wash.
- **Unclamped mix.** The warm part of the floor is added with the mix factor left unclamped (`clamp_factor` off), so the tightest gatherings can climb past a pale tint. Blender's Mix node clamps by default; a rebuilt node tree that forgets this gives flat, pale knots.
- **Extend, Non-Color, Cubic.** The map images must not repeat (a repeat reads as wallpaper), must not be colour-managed (they are data), and are read with cubic filtering.
- **Two volumes must not share a face.** The ray box sits 5 mm inside the water body. Coincident faces of two volumes do not render reliably.
- **Counting rays.** The map script counts with `np.bincount`. `np.add.at` gives the same answer many times slower; keep `bincount` when editing it.
- **A wide floor sun with a shadow-linking collection** left the floor dark and speckled in Cycles 5.2. Light linking alone is enough.
- **The shafts shade what is behind them.** A subject whose sunlight crosses a shaft gets a darker, warmer blotch, and a plain floor gets grey smudges. Widen or move the clear zone toward the sun; see [the rays also shade](recipe.md#the-rays-also-shade).
- **No Light Path node in the ray density.** Hiding the rays from shadow rays (`Is Shadow Ray`) looks like the neat fix for that shade. A test picture that renders in three minutes without the node had not finished after 28 minutes with it.
- **Colours shift under water.** The demo ball is orange (0.95, 0.45, 0.12) and reads yellow-olive in the picture. That is the water absorbing red over the distance to the lens, and it is the same with the rays off. Judge a subject's colour against a render without rays before blaming them.

## Validation and limits

Package checked on 10 November 2026 with Blender 5.2.1 LTS, CPU Cycles, 8 threads, on a machine that was also running other renders.

What was run, each into a fresh folder outside the package:

- The demo at 1280 × 720 and 320 samples: map 65 s, render 760 s. Floor only with the same map: 259 s. Rays only: 1565 s, with two more renders sharing the machine by then.
- `--draft`: 77 s and 134 s on two runs.
- `--subject` at 768 × 432 and 96 samples: 130 s. The ball is evenly lit, with a soft shadow on the floor and no stain. With the clear zone centred on the ball alone (230 mm of ray-free water around its centre) it had carried warm blotches; moving the zone 200 mm toward the sun and clearing 400 mm removed them.
- After the last edits to the package, the millimetre picture of the unit check was rendered again and matched the earlier one pixel for pixel.
- The demo page (`demo/index.html`) in Chrome at 1280 × 720 and at 375 × 812: the three buttons change the picture, its label, note and alternative text; nothing overflows sideways; no console messages.
- Millimetres against `--metres`, the loop wrap and seam, and loop map 1 against the still map, with the results above.
- One train alone (`--train 2`, quarter-size map), rendered floor only at 768 × 432: soft bands running away from the camera and converging.
- A second run into a folder that already held a render: refused, exit code 1, nothing overwritten.

What was not checked:

- The GPU path (`--gpu`). In the work this recipe comes from, GPU renders on Apple Metal occasionally failed at start-up with exit code 133 or 134 and ran on the second try, and a long render now and then stopped without an error. Retry once before looking for a cause.
- Rendering a frame range from the saved `.blend`. Single frames of a loop were rendered through `--frame`.
- Any depth other than 700 mm, a camera looking another way, a stepped or sloping floor, or faster water.
- Blender versions other than 5.2.1.

What does not carry over:

- The floor light and the sun rays were settled by eye, against a reference picture, in a different scene with a close camera and a subject in the water. That approval belongs to that picture. The demo here is a plain pool made to show the mechanism, seen from further away, and has no beauty score of its own.
- The pattern on the demo floor is busier and more net-like than the close view the recipe was tuned for, because a far camera sees many ripple lengths at once. Fewer or weaker gathering spots should calm it; that was not tried here.

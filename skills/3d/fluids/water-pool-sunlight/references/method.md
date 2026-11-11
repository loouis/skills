# The light map: how it is made and what each number does

Read this before changing `assets/demo-pool.json` or writing a spec for another pool.

## What the light has to look like

Pool sunlight fails in a few recognisable ways. Judge a result against these five points, in this order.

1. **Not a pattern.** No tiled crescents, cell edges or marble. A repeated shape still reads as a pattern after it is moved or rotated, so the randomness has to live in the ripples that bend the light, not in shapes drawn on the floor.
2. **Brightness is ray density.** Each ripple is a weak curved lens. Where refracted rays bunch together the floor gets a short bright sliver with a warm-white centre and a soft falloff into the water colour. Followed along its length, a sliver widens, weakens and almost disappears. A few meet in bright knots. No loop reads at one even brightness.
3. **Uneven.** Quiet stretches, faint sweeps, and small areas where the curves gather.
4. **A sunlit wash first.** At thumbnail size, or squinting, you see where the sunlight lands: a soft bright patch that falls away into the water colour. Only at full size do you find the ripples inside it.
5. **Soft, not wiry.** Most of each sliver dissolves into pale, slightly warm light around it. Sharp focus is kept for short gathered sections. Lines cross at varied oblique angles, never as sideways parallel rows.

## The pipeline

```
ripple trains (+ wave groups) --rays, Snell's law--> ray density (sharp map) + the same rays spread wider (soft map)
                                                          |                              |
                                          floor: smooth response x wash        sun rays: the water looks up the
                                          (sharp and soft maps)                soft map along the refracted sun ray
```

One map drives both effects. That is why a shaft of light in the water ends on a bright patch of floor: they are the same rays.

The map is made for a sun straight overhead. The scene then slides every lookup along the real refracted sun direction, so one map serves any sun angle and never needs remaking when the sun moves.

## The surface

The water surface is a sum of a few plane ripple trains:

```
h(x, y) = sum over trains of  A(x, y) * sin(k * (x, y).d + phase + warp(x, y))
```

Each entry in `trains` is one of them:

| Key | Meaning |
|---|---|
| `lam` | Wavelength in millimetres. |
| `dir` | Direction the train travels, in degrees on the floor plan: 0 is +x, 90 is +y. Its crests lie across this direction. |
| `q` | Focusing strength at this depth (see below). Give this, or `amp`. |
| `amp` | Ripple height in millimetres, used as given when present. |
| `warp` | How far the crests bend, in cycles of phase. 0 gives ruler-straight crests. |
| `warp_len` | Length of one bend along the crest, in wavelengths. |
| `base` | Share of the height that is present everywhere, before groups are added. |
| `groups` | `[cx, cy, sigma, gain]` each: a round area (centre and width in millimetres) where this train is taller by `gain` times its height, or calmer when `gain` is negative. |
| `cycles`, `wcycles` | Loops only: whole wavelengths the train (and its bend) moves over the loop. See `loop.md`. |

The other spec keys:

| Key | Default | Meaning |
|---|---|---|
| `name` | | Names the output files. |
| `domain` | | `[x0, y0, size]`: the square of water surface the map covers, in millimetres. |
| `depth` | 700 | Water depth in millimetres. |
| `bins` | 4096 | Cells along a side. Aim for about 1 mm a cell. |
| `photons` | 14336 | Rays along a side. Keep about 3.5 rays a cell each way (12 a cell) or the map turns grainy. |
| `blur_mm` | 1.27 | Blur of the sharp map. |
| `soft_blur_mm` | 8.8 | Blur of the soft map. It stands in for the width of the sun and a little scatter. |
| `seed` | 1 | Fixes the phases and the ray jitter. Same seed, same map. |
| `scale` | 64 | Stored value is density divided by this, so a knot of 50 times the mean does not clip. |
| `margin` | 200 | Rays also start this far outside the domain, so the edges are fed from both sides. |

## Focusing strength

A ripple of height `a` and wavelength `lam` acts as a lens. At depth `D` its strength is

```
q = D * (1 - 1/n) * a * k^2        with k = 2 * pi / lam and n = 1.333
```

`q` below 1: the train only brightens and darkens the floor gently. `q` above 1: its rays cross before they reach the floor and it draws lines. Giving `q` rather than a height keeps a spec meaningful when the depth or a wavelength changes.

The working rule is to **keep every train below 1 on its own and let overlaps do the rest**:

- The fine trains have `q` 0.38 to 0.42 and `base` about 0.35, so on their own, away from any group, they contribute roughly 0.14 each. Seven of them summed stay under 1 over most of the pool: soft light, few lines.
- Groups raise the height locally. Where two or three trains are raised at the same spot the sum passes 1 and lines appear, fine and bright. That is where the light gathers.
- A long swell (`lam` 400, `q` 0.28, `base` 1) moves everything a little, so the fine lines never sit on a regular grid.

The demo spec in this form:

| `lam` | `dir` | `q` | `base` | Role |
|---|---|---|---|---|
| 400 | -10 | 0.28 | 1.0 | swell |
| 130 | -20 | 0.42 | 0.36 | fine |
| 96 | 22 | 0.42 | 0.36 | fine |
| 76 | -160 | 0.40 | 0.36 | fine |
| 60 | 165 | 0.38 | 0.36 | fine |
| 110 | -28 | 0.38 | 0.34 | fine |
| 86 | 30 | 0.38 | 0.34 | fine |

Its groups come in three kinds, and every fine train carries the first two:

- **The sunlit area**: two wide groups (`sigma` 700 and 1000, gain about 0.5). This is the wash, expressed in ripple height.
- **A quiet area**: one group with a negative gain (`sigma` 450, gain -0.3).
- **Gathering spots**: five small groups (`sigma` 170 to 280, gain 0.6 to 1.0), each given to two or three trains only. Different trains meet at different spots, so the spacing of the lines changes from place to place.

## The direction rule

Seen at a low angle under water, the floor is strongly foreshortened: a light line running across the view is squashed into a sideways band, and several of them make parallel rows. Lines that run away from the camera keep their shape.

So, for a camera looking along +y at 25 to 30 degrees onto the floor, keep the crests within 10 to 30 degrees of the depth axis. Crests lie across the travel direction, so the trains travel near plus or minus x: `dir` of 10 to 30, or 150 to 170, either sign. Use both sides so that lines cross.

For a camera looking another way, turn every `dir` by the same angle. For a camera looking straight down the rule does not apply.

Check a train on its own before trusting it:

```sh
python3 scripts/make_light_map.py assets/demo-pool.json /tmp/pool-train-check --train 2
```

This makes only train 2 at full, even strength. Rendered with `--maps`, its lines must run steeply away from the camera and converge. If they lie flat across the frame, the direction is wrong.

## Placing the light in the picture

Group centres and wash lobes are in **map coordinates: the point where the sun ray entered the water surface**, not the point where it lands. With a slanted sun the two differ by a fixed shift.

`scripts/screen_to_lookup.py` converts both ways for a flat floor:

```sh
python3 scripts/screen_to_lookup.py assets/demo-scene.json 640,420 900,600      # pixels -> floor point, map point
python3 scripts/screen_to_lookup.py assets/demo-scene.json --map -760,1420      # map point -> floor point, pixel
```

Work from the picture. Decide where the sunlight should land and where it should stay quiet, read off the map points, and put the wide groups, the quiet group and the wash lobes there. Then add the gathering spots inside the sunlit area. Changing groups means making the map again; changing the wash lobes alone does not (they are in the floor material, see `recipe.md`).

Keep the camera's whole view of the floor inside `domain`, shift included. Outside it the map's edge value is repeated, which shows as smears.

## Making the map

```sh
python3 scripts/make_light_map.py assets/demo-pool.json /tmp/pool-maps
```

Needs numpy only. At 4096 cells the demo map took 65 s, and 342 s on a second run while three renders shared the machine; it peaked at 1.9 GB of memory. It writes:

- `<name>-sharp.png` and `<name>-soft.png`: 16-bit greyscale, density divided by `scale`, mean density 1.
- `<name>.json`: the scale, the domain, percentiles, and the full spec with the phases filled in. The Blender side reads this file.
- `<name>-preview.png`: a small 8-bit picture of the sharp map. It looks like an even net of cells; that is normal. The map is seen from straight above and the picture is not: foreshortening and the floor material turn it into slivers. Judge a render, not the preview.

The script refuses to replace existing files unless `--force` is given. `--bins N --photons N` override the spec for a quicker, coarser map; a coarse map looks more cellular than the full one, so use it to check a setup and not to judge the light.

## What was tried and failed

Each of these was built and rejected on the way to this method. They fail for a reason, not for lack of tuning.

| Approach | How it fails |
|---|---|
| Voronoi distance-to-edge lines | Constant width: reads as cracks or as the tiles themselves. |
| Voronoi F1 minus Smooth F1 ("stars") | Marble or crazy paving, evenly bright. |
| Layered procedural lines, knots, glow, breaks and patches | Still outlines of even brightness, however many layers. |
| Contour lines of a noise field | Loopy spaghetti. |
| A small tiled ray map (650 mm tile), even with a warped lookup | A dense, even wallpaper of crescents. |
| One uniform random-ripple spectrum | Cells everywhere and no quiet stretches. |
| A threshold on density for the warm centre | Hard-edged strokes. |
| Ripple trains travelling along the depth axis | Sideways parallel rows once foreshortened. |

The common thread: anything that draws lines directly gives them even width and brightness. Counting rays gives width and brightness that vary along every line for free, because that is what the light does.

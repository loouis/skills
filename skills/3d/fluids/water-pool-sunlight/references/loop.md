# Moving light that loops

Read this when the floor light and the sun rays have to move.

Nothing in the method changes. The map is made once per frame, and the ripples are moved so that the last frame leads back into the first.

## Why it loops

Each train moves a whole number of wavelengths over the loop. On frame `f` of `N`:

```
phase(f) = phase - 2 * pi * cycles  * (f - 1) / N
warp(f)  = warp  + 2 * pi * wcycles * (f - 1) / N
```

Frame `N + 1` would be frame 1 again, so there is no seam to hide. This only holds while `cycles` and `wcycles` are whole numbers.

The wave groups do not move. The gathered light stays where the still has it; only the lines inside it travel. A still made from the same spec is frame 1 of the loop.

## The spec

Add a frame count, and two numbers to each train:

```json
"loop": {"frames": 168},
"trains": [
 {"lam": 400, "cycles": 1, "wcycles": 0, "...": "..."},
 {"lam": 130, "cycles": 3, "wcycles": 1, "...": "..."}
]
```

`assets/demo-pool.json` already has them, for 168 frames (7 seconds at 24 frames a second):

| `lam` | `cycles` | `wcycles` | Crest speed |
|---|---|---|---|
| 400 | 1 | 0 | 57 mm/s |
| 130 | 3 | 1 | 56 mm/s |
| 110 | 4 | -1 | 63 mm/s |
| 96 | 5 | -1 | 69 mm/s |
| 86 | 6 | 1 | 74 mm/s |
| 76 | 7 | 1 | 76 mm/s |
| 60 | 9 | -1 | 77 mm/s |

Crest speed is wavelength times cycles divided by the loop's length in seconds.

Choosing the numbers:

- **Shorter trains get more cycles**, so all the crests move at a similar speed. Equal cycle counts would make the long swell race and the fine ripples crawl.
- **No train gets zero.** A train that stands still shows as light that does not move while the rest does.
- **Give neighbouring trains different counts** with no common pace, so the picture never visibly repeats inside the loop.
- **These speeds are slow on purpose.** Real ripples of these lengths run at about 300 to 800 mm/s, four to fourteen times faster. Slow reads as calm water and as light drifting. For livelier water raise every count in proportion; faster motion has not been tried with this recipe, so check it before relying on it.
- For a different length, keep the speeds: scale the cycle counts with the duration and round to whole numbers.

## Making the maps

```sh
python3 scripts/make_light_map.py assets/demo-pool.json /tmp/pool-loop \
  --frames 1 168 --jobs 4 --bins 2048 --photons 11264
```

- `--bins 2048 --photons 11264` makes the maps at half resolution (about 2 mm a cell). Moving light hides the difference, and the set is a quarter of the size. The blur is given in millimetres, so it stays the same. Against the full-resolution still, a half-resolution frame 1 correlated 0.997 (sharp) and 1.0 (soft) on the pool this recipe was worked out on.
- `--jobs` is how many maps are made at once. Each needs its own memory; twelve at once took about 8 seconds a map on a 16-core machine, about 20 minutes for the set.
- 168 frames at 2048 cells come to about 1.4 GB.
- The maps land in `<out>/<name>/` as `sharp-0001.png`, `soft-0001.png` and so on, with a `loop.json` beside them. Frames that already exist are kept, so a stopped run can be continued; `--force` remakes them.
- `--frames 1 8` makes a short stretch for a test.

## Using them

One frame through the demo:

```sh
blender -b -t 8 --factory-startup --python-exit-code 1 -P scripts/render_demo.py -- \
  --output /tmp/pool-loop-frame-40 --maps /tmp/pool-loop/demo-pool/loop.json --frame 40
```

In your own scene, `ps.load_light('/tmp/pool-loop/demo-pool/loop.json')` is all that changes. The builders then load the maps as an image sequence that wraps around, on the floor's two textures and on the sun rays' texture. The rays read the same sequence as the floor, so the shafts move with the floor light. Set the scene's frame range to 1 to `N`.

## Checking the loop

- Render frame 1 and frame `N + 1`. They must be the same picture.
- Render every second or fourth frame small, and measure the mean change between neighbours. It should be even all the way round, including from the last frame back to the first. A larger step at the seam means a cycle count is not whole, or the frame count in the spec does not match the number of frames rendered.
- Watch it at full speed before judging. Light that looks right as a still can swim or flicker in motion; if it flickers, the short trains are moving too far per frame, so lower their cycles or add frames.

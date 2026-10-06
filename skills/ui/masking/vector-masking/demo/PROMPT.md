# Vector masking demo prompts

## Minimal

Use $vector-masking to construct masks for the overlapping pieces of this outlined mark, preserving whole shapes, accurate silhouettes, clean joins and the original paths. If the pieces are animated, keep travel flush and open gaps only on landing.

## Recreate

Use $vector-masking to create a dependency-free SVG study of three outlined panels. The front panel is a fixed rectangle; the two whole, rounded rear panels slide symmetrically left and right through separate stationary luminance masks. Keep a 6-unit stroke, use no visible cover fills, and expand each foreground cut-out only after the first travel peak. Provide 8-unit and 14-unit final-gap variants, each with an independently authored static original, and hand over without a visual change. Include forward and reverse playback, a 25 fps frame scrubber, phase jumps, a mask-inspection view and a final-pose comparison. Show the final original by default for reduced motion. Use a warm paper background, dark green ink and simple system typography.

## Remix

Use $vector-masking on our supplied outlined logo. Read its layers and preserve every visible source edge. Reconstruct hidden curves, solve closed tips and root joins, attach moving occluder copies in the correct coordinate space, and taper gap growth to zero where the source lines meet. Export frames and compare the final masked pose against the untouched logo. Choose timing for this mark rather than copying the panel study's spring constants.

## Run and inspect

Open `demo/index.html` directly, or serve this skill folder with:

```bash
python3 -m http.server 4173 --bind 127.0.0.1
```

Visit `http://127.0.0.1:4173/demo/`. There are no network assets or build steps. “Inspect left mask” adds an explanatory background only; turn it off to judge the artwork. “Compare masked pose” jumps to the final pose and switches between the completed mask construction and immutable original paths.

## Export and verify

With Puppeteer available, run from the skill folder:

```bash
node demo/verify.cjs /tmp/vector-mask-frames
```

If needed, set `NODE_PATH` to an existing Puppeteer installation and `PUPPETEER_EXECUTABLE_PATH` to an installed Chrome binary. The script writes 76 forward frames at 25 fps, a contact sheet, mask view, mobile view and a JSON report outside the package. It checks foreground occlusion across both gap variants, flush travel, pixel-identical closed and handover poses, playback in both directions, keyboard scrubbing, reduced motion and narrow layout. Reverse playback traverses the same symmetric poses in the opposite order.

Inspect the contact sheet and zoom into the frames; the checks do not establish correctness for different artwork. This demo covers stationary, straight-sided occluders. It does not demonstrate moving-front chains, organic hidden-curve reconstruction or tapered root joins.

From the repository root, regenerate the 1280 × 720 preview with:

```bash
node scripts/build-previews.cjs vector-masking
```

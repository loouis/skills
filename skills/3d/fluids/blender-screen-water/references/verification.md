# Verification

## Package checks

From the skill folder:

```sh
python3 -B scripts/test_recipe.py --blender blender --ffmpeg ffmpeg
node --test scripts/test_playback.mjs
blender -b --factory-startup --python-exit-code 1 -P scripts/test_blender.py
node scripts/verify_demo.cjs /tmp/screen-water-browser-check
```

Use explicit installed tool paths if needed. The browser check needs Puppeteer and FFmpeg; `NODE_PATH`, `PUPPETEER_EXECUTABLE_PATH` and `FFMPEG` can locate them. These checks use temporary synthetic fixtures. The Blender test configures, saves and reopens the FLIP scene without baking it. Preparation must not start a render, write into the installed skill, or modify an input cache.

Tests cover preparation at 2× resolution, 180 cache hashes, overwrite and missing-input refusal, frame bounds/cache parsing, renderer resume guards, a real tiny FFmpeg encode/decode, partial-repeat mapping, stale play promises, clearing/control timing, configured liquid settings and keyframes, saved cache paths, reflection cards and CPU render settings. Browser checks cover the native stills, narrow layout, detail inspection, keyboard mapping, a real six-second test clip looping to three seconds, reduced-motion poster and cleanup.

The public material-study stills were newly rendered on original generic proxy geometry. They check that the material/bubble pipeline executes; they are not a fresh FLIP bake or evidence that the production motion loops cleanly. No full fluid bake or 360-frame production rerender is required to package the recipe. Newly generated production output still needs the checks below.

## Actual output review

- Record recipe/helper/settings/cache hashes with each job. Confirm all expected frames have one pixel size, the movie decodes fully, and it has 180 frames, 30 fps, six seconds, no unintended audio and the intended colour treatment.
- Watch arrival followed by at least two 3–6 second repeats. Step through 5.4–6.0 and the jump to 3.0. Look for blank re-arrival, reversal, pauses or flashes. A correct frame mapping does not prove a smooth physical seam.
- Inspect native top arrival, central folds, bubble rims, dark openings and lower exit. Compare modes at the same time and exposure. The liquid descends in both; only Hot bubbles rise. Avoid uniform foam and over-soft denoising.
- The short repeat and crossfade may be visible. Air-pocket geometry does not merge, split or solve buoyancy. Describe observed limits instead of claiming thermal realism or universal quality scores.
- Test immediate controller Stop with a still-moving decorative tail, restart during exit, mode switching, focus loss and reduced motion. Controls must not return before clearing; interface text should stay sharp.
- For glass integration, inspect the closest and lowest camera poses for leaks, z-fighting, mirrored/stretched UVs, double reflections, obscured content and brightness changes. Test decoder, memory and display performance on the target hardware.

Keep clean outputs. Make separate marked review copies with frame/time references and identify the actual defect and proposed next change. A preparation test, static material study or earlier render does not approve a new resolution, bake, display or camera move.

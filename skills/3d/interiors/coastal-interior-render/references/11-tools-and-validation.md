# Portable tools and validation

## Requirements

- Blender with Cycles; the fixture and renderer were tested with Blender 5.2.1 LTS on CPU. Discover the receiving machine's executable rather than assuming a workstation path. Check APIs on other versions.
- Python3 and Pillow for review boards/tests. The renderer/generator run inside Blender's Python and do not require Pillow.
- Node.js and Playwright/Chromium only for the optional browser-demo verifier. `NODE_PATH` may point to an existing installation; `BROWSER_EXECUTABLE_PATH` may select an installed compatible Chromium browser. No service, API key or network request is required by these scripts.

Read scripts before adapting them. They are small portable helpers, not the original room's hard-coded builder or a substitute for scene-specific geometry gates.

## Create a generic fixture

`scripts/render_demo.py` starts an empty scene and constructs an original material bench, procedural oak/stone/textile, a bronze arch, two cameras and side lighting. It requires a fresh output directory, saves `study.blend`, reopens it and writes `study-checks.json`. It checks five simple fixture properties plus a reopened thickness check. The cloth is an authored surface sample, not a sofa throw or simulation.

The commands are in [demo/PROMPT.md](../demo/PROMPT.md). Keep output blends and manifests outside the package. Inspect both images before treating the script as validated in a new environment.

## Render an existing scene

Prepare a JSON manifest like [views.example.json](../assets/views.example.json), containing a nonempty `views` array. Each entry names an existing camera and a unique safe slug, plus positive integer width, height and samples. The included example names match the generic fixture only.

```bash
"$BLENDER_BIN" --background --python-exit-code 1 --python "$SKILL_DIR/scripts/render_views.py" -- --scene "$SCENE_FILE" --manifest "$VIEWS_FILE" --output "$NEW_RENDER_DIR" --device CPU
```

Set these variables to explicit paths first. The output directory must not exist. Camera names are preflighted before any image is rendered. The helper suppresses filename/hostname stamp metadata so exported PNGs do not disclose the scene's private path. It hashes the source scene, renders each view to a pending PNG, checks dimensions, renames the completed output and writes `render-manifest.json`. `complete` remains false if the batch fails; completed outputs remain recoverable. Require every `CAMERA_RENDER_COMPLETE`, `RENDER_SET_COMPLETE`, the expected files and clean process exit.

CPU is the default portable test. GPU options are METAL, CUDA, OPTIX, HIP and ONEAPI; the requested backend must expose matching devices. These backend branches were not exercised in the public packaging test. Run one GPU job at a time and verify the actual selected backend. The helper preserves the source scene on disk, uses its colour management and denoising/compositing choices, and does not establish output aesthetic quality.

## Create an annotated board

Inspect the clean image first. Write JSON with a title and nonempty notes. Each note contains `title`, `status` (`open`, `resolved` or `check`), normalized `box` `[x,y,width,height]`, an observed `observation` and a concrete next `action`.

```bash
python3 "$SKILL_DIR/scripts/review_board.py" --image "$CLEAN_IMAGE" --notes "$NOTES_FILE" --output "$NEW_REVIEW_DIR"
```

The tool refuses an existing output directory, validates boxes, wraps headings/body text, extends board height as needed and writes `review.png` plus `review.json`. The original image bytes remain unchanged; the JSON records their hash and original dimensions. It does not invent scores or decide whether an item is resolved. Placeholder notes in [review.example.json](../assets/review.example.json) must be replaced with actual findings.

## Validate the tools

From the skill folder:

```bash
python3 -B scripts/test_tools.py
node scripts/verify_demo.cjs /tmp/coastal-browser-check-fresh
```

The three Python test groups cover immutable source bytes/no overwrite, long-title layout, empty/invalid/out-of-bounds notes, NaN rejection, camera-name preflight, duplicate/path-escaping slugs and invalid sample/dimension types. They are meaningful negative controls for output protection and input validation, not visual correctness tests.

The browser verifier checks native image loading, inspection-box visibility, view/download switching, mobile overflow and runtime errors, then exports desktop/detail/mobile evidence. Inspect those screenshots too. It writes `preview.jpg` at 1280×720; copy that into `demo/preview.jpg` only after review.

## Packaging evidence and limits

The package was tested with two fresh 1280×720 CPU Cycles outputs at 64 samples, saved-scene reopening, source/output hashes, Python negative controls and actual browser inspection. The demo's stone remains deliberately quiet, its grain procedural and its cloth simplified. No production-room visual score, full furniture rebuild, cloth simulation, complete collision test or GPU backend validation is claimed by these tests.

For a real room, add project-specific evaluated bounds/contact/attachment/UV/preservation checks and the full camera review described in [08 · Review](08-review-and-delivery.md). Never promote this fixture's five property checks into proof of apartment realism.

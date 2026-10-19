---
name: coastal-interior-render
description: Build and refine editable Blender/Cycles coastal apartment interiors with warm timber, restrained stone, natural daylight and tactile furniture. Use for premium beachfront kitchen/living scenes, Burly- or MIRA-inspired art direction, practical layout, kitchen construction, upholstery, throws/fringe, glazing, balconies, reference comparison and annotated realism reviews. Includes detailed modelling, material, lighting and failure-recovery methods. Do not use as a promise of an automatic quality score, a construction specification or a substitute for a requested direct 3D render.
---

# Coastal Interior Render

Create a plausible luxurious home, then photograph it in 3D. The default direction combines warm coastal materials with architectural restraint: pale oak, quiet ivory stone, mineral whites, flax upholstery, a deeper greige rug, small tobacco/terracotta accents, muted champagne metal, full-height sheers and a coherent distant outlook.

## Start here

1. Read the receiving project's instructions, status, brief, selected scene and last rejected review. Preserve accepted work. A supplied floor plan, product choice or user correction takes precedence over these defaults.
2. Read [style and references](references/01-style-and-reference-study.md), [layout](references/02-layout-and-architecture.md) and [review protocol](references/08-review-and-delivery.md) before proposing the scene. Inspect actual reference pixels; a prose summary is insufficient.
3. Establish the output: editable scene plus direct Cycles images by default. If the user explicitly requests another renderer or an AI concept, honour that and label the result accurately. Never replace a requested editable reconstruction with an AI image edit.
4. For “I want a scene”, proceed with a labelled original kitchen/living concept in this palette. Use the starter dimensions below only if no plan is supplied. Ask early only for information that materially blocks the work, such as an exact property outlook for a site-faithful sales image. Continue independent modelling while waiting.
5. Record a brief, a reference/provenance manifest, a versioned scene, named cameras and a review ledger. Keep published facts, visible observations and proposed choices distinct.

## Default scene brief

- One connected kitchen/living room; the island is the main subject and the living space remains clearly legible.
- Generous routes around occupied seating; everyday traffic avoids the cook's work aisle.
- Pale timber joinery, honed mineral island, coordinated premium appliances, usable discreet pulls, carefully aligned grain and joints.
- Substantial sofa with compression and tailoring, modest exposed timber supports, a small muted accent cushion and a broad naturally folded throw with full attached fringe.
- Side daylight with cooler sky fill, useful recess shadows and clear separation between stone, timber, textile, metal and glass.
- Curtains with plausible tracks, attachment and floor relationship. Terrace depth, supported glass, return rails and a distant horizon.
- Restrained objects: two well-modelled art books, one shallow vessel and one small glass or metal accent. Preserve working surfaces and room usability.

Starting planning concept, not a minimum standard: 9.40 × 7.80 m living zone, 3.20 × 1.05 m island, 900 mm island height, equal 70 mm stone top/ends, 400 mm knee recess, about 3.0 × 1.0 m sofa, 2.80 m terrace depth. Test the plan rather than scaling these blindly into smaller rooms. See [layout](references/02-layout-and-architecture.md).

## Production sequence

### 1. Study and block out

Choose a coherent reference family. Compare floor plans within similar size/household groups. Model walls, slabs, glazing, terrace, island and occupied furniture envelopes in metres. Check routes, door use, sink/prep/hob sequence, storage, views, sunlight and privacy. Save hero, reverse, overhead and working-side cameras before detail modelling.

### 2. Resolve construction

Read [kitchen](references/03-kitchen-construction.md) and [furniture](references/04-furniture-and-styling.md). Make slabs level and equally thick; build convincing joints, actual cabinet reveals, usable handles and connected supports. Inspect the sink from above and from the cook's aisle. Capture all original multipart asset transforms before placement. Measure the evaluated geometry, including hardware and upholstery projections.

### 3. Build tactile materials and soft furnishings

Read [materials](references/05-materials-and-uv.md) and [textiles](references/06-textiles-drape-and-fringe.md). Establish broad form and gravity first, seams second, yarn relief third, tiny fibres last. Use physically scaled UVs and correct colour/data maps. Grain follows each member and every exposed face. Preserve the full preferred fringe while repairing its attachment.

### 4. Light the actual architecture

Read [lighting and camera](references/07-lighting-reflections-camera.md). Fix the colour pipeline, build the exterior occluders, then establish sun/sky balance. Add the minimum justified photographic fill. Record source dimensions, placement, ray exclusions and exposure. Diagnose geometry, normals, material and reflected environment separately; use matched source-off controls for unexplained wall patches or pale glass.

### 5. Verify, render, annotate, improve

Run construction/contact/preservation gates before assigning an appearance score. Render the saved scene. Inspect thumbnail, whole-room, matched reference and native detail views. Make separate numbered boxes with an observable defect, likely cause, next change and verification camera. Fix the highest-impact defect, change one family at a time, and repeat. A newly discovered defect or user correction reopens the relevant score.

Do not claim a 9.5 or 10 because the user requested it, tests passed, polygon count rose or time was spent. The source process remained below the whole-room benchmark; see [iteration lessons](references/09-iteration-lessons.md). Keep working toward the requested target while useful improvements remain, report actual limitations, and never manufacture a pass.

### 6. Deliver a reproducible selection

Reopen the selected scene, verify packed resources, render all affected cameras, inspect them, then publish the selection. Preserve clean outputs, rejected versions, separate annotations and source attribution. A local material test is not a full-room delivery. Update the receiving project's status and review ledger with the exact selected version and unresolved items.

## Read by task

| Task | Required detail |
| --- | --- |
| Visual direction, reference use, rooms beyond kitchen | [01 · Style](references/01-style-and-reference-study.md) |
| Plan, circulation, practical sales brief, balcony/door options | [02 · Layout](references/02-layout-and-architecture.md) |
| Island, drawers, sink, tap, appliances | [03 · Kitchen](references/03-kitchen-construction.md) |
| Sofa, selected stool reconstruction, tables, books, plants | [04 · Furniture](references/04-furniture-and-styling.md) |
| Stone, oak, metal, glass, texture maps and packing | [05 · Materials](references/05-materials-and-uv.md) |
| Throws, folds, waffle weave, fringe, curtains and rug | [06 · Textiles](references/06-textiles-drape-and-fringe.md) |
| Sun, fill, reflections, wall spill, camera and background | [07 · Lighting](references/07-lighting-reflections-camera.md) |
| Gates, scoring, annotations, render evidence and handoff | [08 · Review](references/08-review-and-delivery.md) |
| What failed, why, and what to preserve | [09 · Lessons](references/09-iteration-lessons.md) |
| Detailed selected recipe and its limits | [10 · Recipe](references/10-selected-recipe.md) |
| Tools and tested examples | [11 · Tools](references/11-tools-and-validation.md) |
| Rights, historical sources and portability | [12 · Provenance](references/12-provenance-and-scope.md), [source links](REFERENCES.md) |

## Included tools

- `scripts/render_views.py`: render a named-camera manifest from an existing scene into a fresh directory; explicit CPU/GPU choice, preflight, saved-scene hash and per-image completion markers.
- `scripts/review_board.py`: separate numbered review board from a clean render and JSON notes; preserves source bytes and records its hash. Requires Pillow.
- `scripts/render_demo.py`: original procedural material vignette for this public skill. Demonstrates the toolchain, not a furnished apartment or a benchmark-quality production scene.
- `assets/review.example.json` and `assets/views.example.json`: input formats. Replace camera names and defects with actual observations.

The skill is the production method, not a hidden scene library. External references and assets must be obtained with appropriate rights. The complete scene needs modelling and visual review; the demo is deliberately a small independent study.

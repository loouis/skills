# Recreate or use the skill

## Minimal scene request

Use $coastal-interior-render to create a warm, restrained beachfront kitchen and living room. Build an editable Blender scene with pale timber, quiet stone, realistic furniture and fabrics, natural light and a coherent terrace. Use the skill's defaults where no plan is supplied, record assumptions, and inspect/annotate each iteration without inventing a passing score.

## Refine an existing scene

Use $coastal-interior-render on the selected scene in this project. Read the existing brief and review ledger, preserve accepted furniture and layout, compare actual reference images, then fix the highest-impact realism defects. Deliver clean direct renders and separate annotated evidence.

## Recreate this public demo

Create the skill's original generic material vignette and render both saved cameras. This is a procedural stone/timber/metal/fabric bench, not a full apartment, cloth simulation, product replica or completed quality benchmark. No external textures are needed.

From the skill folder, with an absolute Blender executable and fresh output directories:

```bash
"$BLENDER_BIN" --background --python-exit-code 1 --python "$(pwd)/scripts/render_demo.py" -- --output /tmp/coastal-demo-source
"$BLENDER_BIN" --background --python-exit-code 1 --python "$(pwd)/scripts/render_views.py" -- --scene /tmp/coastal-demo-source/study.blend --manifest "$(pwd)/assets/views.example.json" --output /tmp/coastal-demo-renders --device CPU
```

Set `BLENDER_BIN` to the installed executable first. Paths here are explicit temporary examples; choose unused locations. Inspect the outputs before copying `hero.png` and `detail.png` into `demo/`. Keep `.blend`, logs and test manifests outside the public package. Rebuild `demo/preview.jpg` from the real browser at 1280×720. The public images are untouched Cycles PNG outputs; browser inspection boxes are separate SVG elements.

## A useful variation

Keep geometry and camera fixed. Compare broad diffuse sky light against a more directional side light, then annotate stone highlight width, metal reflection structure and cloth shadow depth. Do not change materials at the same time or score the fixture as a whole-room result.

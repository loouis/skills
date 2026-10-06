---
name: blender-polished-chrome
description: Create realistic chrome and mirror-polished metal renders in Blender Cycles. Use for polished stainless steel, chrome plating, satin-looking metal, harsh reflection bands, and studio material or lighting refinement while preserving product geometry.
---

# Blender polished chrome

Make polished metal read through sharp, continuous reflections with controlled light and dark areas. Separate **material identity**, **surface finish**, **reflection environment**, and **geometry** when diagnosing a render.

## Work from the existing scene

1. Establish the actual material and requested scope. “Chrome-like” may describe mirror-polished stainless steel, not chrome plating. Preserve confirmed metal identity; ask only when an unresolved identity would change the work. Do not infer an alloy grade or manufacturing finish standard from appearance.
2. Preserve the master and existing renders. Save independent, named `.blend` revisions. Record the camera, exposure, color management, geometry/normals and out-of-scope materials before changing them. See [verification](references/verification.md) for saved-scene checks.
3. Render a small baseline. Copy only the intended material graphs, reuse each copy across its intended slots, and inspect shared mesh data and nested node groups before editing them. Do not mutate materials on unrelated instances.
4. Hold camera and exposure constant. Change one cause at a time: roughness first, then reflection environment if necessary. Use actual Blender renders; do not replace product geometry with generated images or blur away defects.

## Diagnose before adding detail

- **Sharp but grey:** identify what the metal reflects. A broad grey floor can resemble satin even at low roughness. Temporarily hide the floor from glossy rays as a controlled diagnostic, then restore it. For the retained studio setup, keep the floor reflected and introduce a broad feathered dark card only where useful.
- **Soft everywhere:** inspect roughness, normal/bump amplitude, sampling, denoising and focus. More lights or exaggerated scratches will not repair a soft finish.
- **Hard rectangles or finite stripes:** broaden, feather, move or rotate reflection panels. Follow the reflection over the entire object, including cylinders, recesses, side ridges and base.
- **Faceted silhouettes or distorted edges:** inspect mesh, bevels and evaluated normals. Keep geometry changes separate from material-only work; get the needed scope before modifying the model.

Read [material and reflection recipes](references/recipes.md) when tuning nodes or building cards. The supplied [reflection-card helper](scripts/reflection_card.py) creates a UV-feathered plane without changing existing objects, materials, selection or render settings. It is optional; equivalent node work is fine.

## Refine and inspect

1. Preserve useful HDR/world lighting and broad upper diffusion. Add tonal depth without flooding the product with fill or losing real edge separation.
2. Use restrained polish values as starting points, not measured properties: body/casting roughness around `0.035 ± 0.003`, edge roughness around `0.050 ± 0.003`. Retain the established reflectance and coat state when changing finish. Adapt to the actual object and references.
3. Keep the product's contact shadow. A reflection card hidden from camera and direct shadow rays can still alter indirect illumination; describe it as art-directed reflection control, not physically isolated lighting.
4. Compare a few small drafts, then inspect native detail renders at 1:1 and a complete frame. Verify head/upper forms, full body and base; a good hero crop can conceal a poor lower reflection. See [troubleshooting](references/troubleshooting.md).
5. Reopen the saved result and verify intended changes plus preserved invariants. Automated preservation checks do not certify photorealism. Report concrete visible defects and remaining uncertainty, without invented realism scores.

## Deliver

Provide the independent scene, native render(s), concise settings/change notes, and matched comparison where useful. Keep version-specific image and scene downloads paired. Use resolution and quality appropriate to the output; [verification](references/verification.md) includes a high-quality starting configuration.

The [generic demo](demo/index.html) compares roughness and floor-reflection control on original geometry. Its [recreation prompt](demo/PROMPT.md) and [Blender generator](scripts/render_demo.py) require no source project, downloaded model or HDR asset. The packaged helper was exercised in Blender 5.2.1; verify socket/API differences on other versions rather than claiming untested compatibility.

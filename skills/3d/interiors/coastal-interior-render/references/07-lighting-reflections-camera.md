# Daylight, reflections, camera and the outside

## Establish one light story

Choose sunny or soft daylight deliberately. For sun, window frames, columns and slab overhangs must cast related shadows. For soft weather, use broader gradients instead of inventing hard patches. Let the room become darker away from the opening, while reflected light keeps useful detail. Warm sunlight and a slightly cooler sky can separate surfaces without an orange global grade.

Set the scene-linear/display pipeline first, record view transform/look/exposure and keep them fixed during matched tests. In the source workflow this was Blender/Cycles; version-specific sockets and colour transforms must be checked in the receiving installation.

Build the actual surrounding architecture and off-camera surfaces. A tap needs bright window shapes and darker room forms to reflect. Honed stone needs softer highlights than metal; glazing needs transmission and angle-dependent reflected cues. The image cannot be solved by albedo alone.

## Lighting order

1. Start with world/sky and sun through the modelled glazing and overhang.
2. Check that sun rays can reach the intended surface. Trace the path; inspect glazing/shadow settings and whether a background plate blocks light.
3. Set useful key-to-fill separation and protect pale surface detail. Look at the island, sofa and floor simultaneously.
4. Add only necessary local photographic bounce/fill and architectural LEDs. Keep fixture geometry plausible; a photographic aid is not a permanent fitting.
5. Check every corner of each area source against room/wall bounds. A source centre inside the room does not prevent a corner sticking through a wall.
6. Inspect glazing and glossy surfaces for visible sources, rectangular ghosts and over-bright reflections. Any ray visibility exclusions are declared artistic controls, not a claim of fully physical site illumination.

The selected case used an 18 W seating return excluded from glossy/transmission rays, and area-source transmission exclusions elsewhere. This preserved a clear outlook but is a controlled photographic treatment. Record such choices for reproducibility; do not hide them in a “physically accurate” claim.

## Diagnose unexplained patches with matched controls

A narrow wall strip beside the tall cabinet survived sun-off, disappeared when appliance fill was off, and survived disabling that fill's glossy contribution. This isolated diffuse spill/bounce from the local fill. Reducing that source from 7 W to 0.5 W corrected the wall while preserving the scene.

Use this diagnostic sequence for new problems: save baseline, same camera/exposure/samples; disable candidate source; separate diffuse/glossy/transmission contribution where supported; inspect geometry/normals if the patch remains. Change the identified cause only. Do not darken the wall material or retouch the output to hide a lighting defect. Recheck the appliance, whole kitchen, hero and glazing after the fix.

The source's sun-energy 8 versus 16 control showed that 16 lost pale detail; 8 retained form. This is not a portable outdoor sun specification. Light size, distance, units, environment, geometry, colour pipeline and exposure determine the result together. See [recipe](10-selected-recipe.md) for exact historical values and limits.

## Camera

Start around 1.25–1.50 m above finished floor and roughly 28–35 mm full-frame-equivalent for an architectural hero. These are proposals, not measured reference camera settings. Use the actual sensor/lens relationship. Move the camera before reaching for an extreme wide lens. Keep verticals composed, avoid stretched edge furniture, and retain useful foreground/middle-ground/background separation.

Use longer focal lengths for product/material details where appropriate. Most room views benefit from broad depth of field; strong blur belongs to a deliberate detail shot. Avoid tap/mullion tangencies, horizon crossing a key object, cropped island ends and a table cut off by a “better” lens.

Save reverse/overview and functional cameras early. A camera placed inside storage or a wall is a failure, even if it would make a nice composition without the architecture. Do not move furniture into unrealistic positions just to clear the lens. Review a changed framing against the complete brief.

## Exterior depth and background

Sea directly beyond the floor with oversized waves reads as water at terrace level. Explain elevation with visible terrace depth, rail/front and side returns, beach/land below where appropriate, a coherent horizon, reduced distant wave scale and atmospheric contrast.

For a real property, use verified site orientation, floor elevation, outlook and appropriately licensed photography/geometry. An east-facing Gold Coast view generally suggests morning for a visible sun over the sea; verify actual aspect instead of placing a sunset disc by habit. Dubai locations vary considerably in orientation.

When the user authorises a temporary illustrative plate, label its provenance and limits. The developed coast was an AI-generated illustration, not a verified view. A distant plane position was a rendering control, not shoreline setback. Keep background generation/editing separate from the direct interior render and follow the applicable image-generation workflow when making new plates.

Match horizon and projection in the scene, preserve original source pixels and record UV/camera mapping. Test full coverage from every saved camera, including low sofa and overhang views. A plate may cover the hero but expose its lower or upper edge in another camera. Check rays through visible glazing against plate bounds; a coverage pass does not prove resolution, photographic truth or terrain fidelity.

## Output and finishing

Preserve meaningful shadows under furniture and overhangs. Pale highlights can be bright but should retain useful surface form. Avoid uniformly raised exposure, excess bloom, clarity halos and an equally sharp/contrasty exterior. Inspect raw versus denoised textile and glass detail. If post-processing is part of the brief, retain raw output and document it; do not present an altered image as untouched Cycles pixels.

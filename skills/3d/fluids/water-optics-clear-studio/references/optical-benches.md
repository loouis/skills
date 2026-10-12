# Optical benches

`assets/optics.py` is the procedural source; `assets/optics-settings.json` holds the final configurations. No scene, texture, font or external asset input is required. Geometry is in Blender units (BU), with separate scene unit scales. Do not convert a measurement in millimetres into those coordinates without also accounting for scale.

| Setting | Droplet | Air cavity | Fold |
| --- | --- | --- | --- |
| Metres per BU | 0.1 | 0.3 | 1 |
| Camera location BU | (0,0,.55) | (0,0,.55) | (0,-.20,.24) |
| Camera target BU | origin | origin | (0,0,.02) |
| Orthographic scale BU | .065 | .065 | .145 |
| AgX look | Medium High Contrast | Medium High Contrast | Very High Contrast |
| Exposure | 0 | 0 | +.85 |
| Original final pixels | 1600² | 1600² | 1600² |
| Samples ceiling / time cap | 1536 / none | 1536 / none | 2048 / 240s |

The camera's 100 mm lens field does not set perspective in orthographic mode. Render time limits do not guarantee convergence or byte-identical rerenders.

## Boundaries

The drop starts from a closed 192-segment, 128-ring UV sphere of radius .016 BU with low-frequency asymmetric deformation, Y×.96 and Z×.93. Its normals face from water into air.

The cavity uses reversed sphere faces, with additional X asymmetry, Y×.87, Z×.38 and a shallow centre curl. It sits inside a closed surrounding water body extending −5…+5 BU. The camera is inside that water. The negative cavity volume is intentional; the outer body remains positive. This prescribed pocket is not a stable bubble simulation. Use an asymmetric grid control to check orientation, not a symmetric pattern alone.

The fold has a 1601×1601 front grid over −.15…+.15 BU in X/Y, closed sides and rear at Z=−.045. Front faces are smooth; sides/rear flat. Broad sinusoidal faces and smooth crests dominate eleven small mixed capillary terms. The upward diffuse receiver is at Z=−.014 inside the water, with colour(.45,.58,.68), roughness1. Keep this dense surface even when testing fewer image pixels; changing both confounds the test.

## Common material and render values

- White Glass BSDF, Beckmann, IOR1.333, roughness0; no water bump or volume nodes.
- Cycles: total/transmission16, glossy8, diffuse4, transparent8, volume0; glossy filter1.0; unclamped direct/indirect; reflective/refractive caustics enabled.
- Adaptive threshold.004, minimum32, seed41; OpenImageDenoise, RGB_ALBEDO_NORMAL, ACCURATE prefilter.
- Blackman–Harris width1.0; full focus; opaque film; RGB16-bit PNG.
- Raw and denoised PNGs share a render. The raw PNG has the display transform applied; it is **not scene-linear radiometric data**.

## Reflection fields

For drop/cavity: left card location(−.12,.11,.16), size(.10,.17), input8; right(.16,−.02,.08), size(.035,.18), input3. The two feather-axis values multiply, so their centre peaks are64 and9, not8 and3. The small disk glint is at(−.05,.065,.095), diameter.008, energy.2. Rear grey fields at X±.11,Z−.065 have size(.10,.30), colour(.8,.9,1), emission.045. The cool refracted background is at Z−.13; source code includes its smooth colour field and the world’s three directional lobes.

For fold: left/right card inputs1.5/.7 (peaks2.25/.49), strip at(0,.20,.24), size(.28,.035), input3 (peak9). Constant world(.82,.9,1), strength.004. Disk caustic source at(−.09,.10,.40), diameter.006, energy9; water caster, diffuse receiver and light caustic flags all enabled. Global caustic switches alone do not establish this arrangement.

The portable demo explicitly uses CPU. Earlier isolated studies used Metal; a later product pool differed across backends under a matched control. Validate the actual scene/backend before attributing unexpected optics solely to geometry.

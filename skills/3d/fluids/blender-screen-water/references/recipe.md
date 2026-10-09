# Simulation and look recipe

These are art-direction parameters, not physical dimensions or manufacturing specifications. Exact formulas are also preserved in the bundled generators.

## Coordinates and FLIP

The screen is XY, +Y top, −Y down; camera looks along −Z. Gravity pushes down and toward the backing. This is a water-wall study, not plumbing.

| Property | Baseline value |
|---|---|
| Frames/fps | 1–180 / 30 |
| Gravity | `(0,-3.8,-2.0)` |
| Domain centre/dimensions | `(0,0,.14)` / `(.60,2.12,.40)` |
| Resolution/mesh scale | 256 / 2 |
| Cache | ALL, mesh BOBJECT, data UNI, external `cache/` |
| FLIP ratio/randomness | .94 / .08 |
| Mesh radius/smoothing | 1.45; positive/negative smoothing 1; IMPROVED generator |
| Time scale/substeps/CFL | .50 / min 2, max 6 / 2 |
| Diffusion | enabled, viscosity base 1/exponent 6, surface tension .3 |
| Boundary flags | `use_collision_border_front=False`, `use_collision_border_top=False` |
| Inlet centre/dimensions | `(0,1.005,.055)` / `(.565,.075,.13)` |
| Flow | LIQUID INFLOW, initial velocity enabled, surface distance 1.5 |
| Lip | 64-side cylinder, radius .07, depth .66, centre `(0,.91,-.035)`, rotation `(0,π/2,0)`, COLLISION effector |

Inlet/lip are hidden in renders. Key inlet velocity every three frames (`range(1,181,3)`):
```python
(.10*sin(frame*.095), -.48-.11*sin(frame*.073), .12+.035*sin(frame*.067))
```
This changes crossflow without reversing descent. Bake uses eight fixed CPU threads and refuses an existing revision directory. Relocating the BLEND requires the external cache path to be updated in a fresh scene copy.

## Mesh reconstruction

Decompress each `.bobj.gz`: little-endian int32 vertex count, float32 xyz vertices, int32 normal count and normals, int32 triangle count and int32 indices. Renderer skips cached normals and smooth-shades reconstructed triangles. Water object location is `(0,0,.14)` and uniform scale `2.12`. This scale is a cache convention, not product dimensions.

## Water and depth

| Component | Value |
|---|---|
| Water RGB / roughness | `(.985,.995,1)` / .008 |
| Water IOR / transmission | 1.333 / 1 |
| Capillary detail | Object coords → 4D Noise, scale 110, detail 2.5, roughness .6 |
| Bump | strength .20, distance .0008 |
| Noise time | `W=frame/30*.18` |
| Backing centre/dimensions | `(0,0,-.063)` / `(.70,2.20,.015)` |
| Backing RGB/roughness/specular | `(.0015,.002,.0025)` / 1 / 0 |
| World RGB/strength | `(.18,.20,.23)` / .10 |

A bright or specular backing and overly broad reflections can flatten folds to grey. Keep clear dark openings between silver edges. Avoid flat noise, blue jelly, milky fog and uniform foam.

## Reflection lighting

Three emissive planes point at `(0,0,.10)`, colour `(.94,.97,1)`. Hidden from direct camera/shadow rays, still illuminating/reflected/refracted. Strength is an emission multiplier, not area-light wattage.

| Plane | Position | Size | Strength |
|---|---|---|---|
| Silver left | `(-.7,.2,1.25)` | `(.60,3)` | 9 |
| Silver right | `(.8,-.3,1)` | `(.30,2.2)` | 11 |
| Soft fill | `(0,.4,2.8)` | `(3,4)` | .45 |

UV emission falloff is `(.5+.5*cos(2π*(u-.5)))*(.5+.5*cos(2π*(v-.5)))`, zero at edges to avoid hard rectangular cutoffs. Keep camera/lights/exposure/main surface shared between Hot and Cold.

## Bubble geometry

Air material: RGB 1, roughness .035, transmission 1, relative IOR `1/1.333`. Template: subdivision-2 icosphere. Deterministic `random.Random(82)`. Seed count is not the visible bubble count; bounds, birth threshold and surface hits remove candidates.

| Property | Cold | Hot |
|---|---|---|
| Candidate seeds | 3000 | 9000 |
| Cluster X centres | `[-.175,.14,-.035]` cycling by seed | same |
| Gaussian X width | .048 | .063 |
| Y | `1.01-.48*age-1.90*age²` | `-1.03+.70*age+1.55*age²` |
| Birth threshold | −.42 | −.72 |

Radius `.0014+random()²*.0060`; individual phase, angle, variation. At `t=(frame-1)/30`, `age=(t*.5+phase*1.17)%1.17`, `birth=t*.5-age`. Skip Y outside `[-.96,.94]`; skip if `sin(birth*9+phase*2+angle*.15)` is below threshold. X: `x0+.015*sin(age*8+angle)+.02*sin(birth*4)`; skip `abs(x)>.27`.

Build world-space BVH from that frame's liquid. Raycast from `(x,y,.40)` along `(0,0,-1)` length .6. Skip misses or hits below Z=−.048. Bubble centre Z is `hit.z-radius*.8`. Sphere axis factors are `(1+.14*sin(angle+age*3),1+.20*variation,.86)` times radius.

The sheet descends in **both** modes; only Hot bubble motion rises. Bubbles do not physically merge/split, solve buoyancy or create vapour. Preserve mixed scale, clusters and dark gaps instead of maximizing seed density.

## Source camera and rendering

Camera `(0,0,4)`, zero rotation, ORTHO scale 1.80. Output 480 × 1800 (4:15). This is the water source camera, separate from product camera moves.

Cycles 128 samples; denoising; adaptive threshold .015/min 24; bounces total 10/transmission 8/glossy 6; reflective/refractive caustics off; indirect clamp 3; seed 29, animated seed off; persistent data. RGB 8-bit PNG. AgX, Medium High Contrast, exposure 0, no DOF enabled.

The portable renderer defaults to CPU. Choose `--device METAL`, `CUDA`, `OPTIX`, `HIP` or `ONEAPI` only on a supported host. For Metal, set `kernel_optimization_level='OFF'` before device discovery and enable only Metal devices; the job commands include `CYCLES_METAL_DISABLE_BINARY_ARCHIVES=1`. Unsupported devices fail explicitly. GPU output and bakes may differ across hardware and Blender versions; preparation does not establish visual parity.

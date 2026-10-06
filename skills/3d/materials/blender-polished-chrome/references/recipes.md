# Material and reflection recipes

## Identity and finish are independent

For an uncoated opaque metal in Principled BSDF, Metallic `1` is a useful starting point. Base Color controls metallic reflection tint; Roughness controls its spread. Retain a confirmed reflectance or measured material model when adjusting polish. Do not make steel brighter by silently changing it to chrome, silver, white paint or a coated dielectric.

For **stainless steel**, the generic demo uses linear RGB `[0.56, 0.57, 0.58]`, Metallic `1`, Coat Weight `0`. This is an artistic near-neutral approximation, not an alloy measurement. For **chrome plating**, use a chromium reflectance reference or the approved chrome material already in the scene, then tune its finish separately. Do not reuse the stainless numbers and label them measured chrome. Both can have mirror-like finishes; neither needs invented brushing or scratches.

Enter linear values through Python sockets or use the appropriate color-space conversion in the UI. An sRGB hex value is not numerically interchangeable with linear RGB. Blender roughness is not a physical surface roughness measurement such as Ra.

## Restrained finish

| Control | Example starting point | Adaptation |
| --- | --- | --- |
| Body and recessed casting roughness | `0.035 ± 0.003` | Narrow variation; avoid a visibly mottled mirror |
| Edge roughness | `0.050 ± 0.003` | Preserve real edge definition; do not erase bevels |
| Fine bump | Strength `0.08`, Distance `2e-7` at metre scale | Often unnecessary at delivery scale; do not force visible noise |
| Existing casting bump | Strength `0.10`, Distance `2e-6` at metre scale | Reduce excessive inherited bump, preserving its texture/link |

These are artistic settings from a successful studio study, not universal material constants. Noise wavelength, object scaling and mapping matter as much as amplitude. Verify the scene's physical scale and test at native pixel size. Start smooth if no microtexture is needed; avoid a procedural texture stack solely to look “realistic.”

Copy each intended material once and map old material → new material so shared slots stay shared. `Material.copy()` retains references to nested node groups and images: copy a nested group before changing it if it has out-of-scope users. A mesh's data-linked material slots can also be shared across instances. Use object-linked slot overrides when isolating an instance; do not casually duplicate or edit its geometry.

If Roughness is linked, changing its socket default does nothing. Inspect its upstream graph and adjust a copied remap/ramp or insert a deliberate remap. Preserve unaffected color, normal, displacement and coat paths. Do not automatically overwrite linked values with constants.

## Feathered floor reflection card

Use only after the floor contribution is established. Keep the floor material and glossy visibility intact; start with the existing HDR/world and upper diffusion unchanged.

Construct this material:

1. UV → Separate XYZ → separate **B-spline** grayscale Color Ramps for X and Y.
2. Multiply X and Y values into an opacity mask.
3. Feed mask into Mix Shader: input 1 = white Transparent BSDF, input 2 = Emission.
4. Set Emission to linear grey `0.012`, strength `1` for a dark card. This is low emitted radiance, not a measured black diffuse material.
5. Connect Mix to Material Output. Exclude the plane from camera and direct shadow rays; keep glossy visibility. Leave the product's own ray visibility unchanged.

Example mask stops, expressed as `(position, opacity)`:

```python
x_stops = [(0, 0), (.25, .85), (.70, .85), (1, 0)]
y_stops = [(0, 0), (.10, 1), (.90, 1), (1, 0)]
```

B-spline interpolation rounds and blends the control values; they are not guaranteed flat plateaus or exact zero at mesh edges. Make the plane broad enough that its finite boundary does not interrupt a visible reflection. Enlarge or move it if an edge remains apparent; do not assume feathering makes every placement seamless.

For an upright object of height **H**, a starting card footprint is approximately **2.3H × 4.6H**, parallel to the floor, just above it (about **0.002H** to avoid coincidence). Offset roughly **2.3H toward the camera** and **0.3H sideways** in the floor plane. These ratios describe one useful starting arrangement. Follow actual reflected rays and adapt to camera elevation, curvature, object extent and floor orientation. Keep it clear of the object's contact area.

The helper uses local UV X/Y and local +Z aimed at `target`. Set `roll` in radians when the long axis needs rotating within the plane. Example for a metre-scale, Z-up scene with a camera facing from negative Y:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path("path/to/blender-polished-chrome/scripts").resolve()))
from reflection_card import create_card

H = 0.35
card = create_card(
    "Floor reflection v01", size=(2.3 * H, 4.6 * H),
    location=(.3 * H, -2.3 * H, .002 * H),
    target=(.3 * H, -2.3 * H, H),
)
```

Calls create a new object with a unique name; they never replace an earlier card. Keep the returned handle for adjustments. The helper uses explicit UVs so a flat plane does not depend on generated-coordinate bounds. It does not save files, reset scenes or change global preferences.

## Broad upper diffusion

The same helper can make a brighter graduated panel: supply `tone_stops` such as `[(0, .08), (.35, .6), (.7, 1), (1, .15)]` and increase `strength` gently. Tone varies along local X independently of the X/Y opacity feather. Aim a large panel at the upper form and move/rotate it until its falloff follows the curve. Treat these numbers as a new lighting experiment, not a prescribed copy of a particular rig.

Favor broad continuous highlights with a dark-to-light transition and enough dark reflection to reveal the silhouette. A huge bright fill can flatten ridges; a short narrow dark flag can become a finite stripe on a cylinder. Evaluate the complete object after every panel change. Emission/transparent panels and ray exclusions affect light transport; they are studio art direction and can influence diffuse/indirect light too.

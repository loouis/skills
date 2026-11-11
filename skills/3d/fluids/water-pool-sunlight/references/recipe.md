# The Blender side: floor light, sun rays, water and lights

Read this before putting the recipe on your own scene or changing a number in `pool_sunlight.RECIPE`.

`scripts/pool_sunlight.py` holds the builders. `scripts/render_demo.py` is a complete, small example of calling them.

## Conventions

- Z is up. The water surface is the plane `z = water_z` (0 by default).
- Every length in the recipe is in millimetres. `upm` is Blender units per millimetre: `1.0` when one unit is a millimetre, `0.001` when one unit is a metre. Each node tree turns world position into millimetres first, so the recipe's numbers do not change with the scene's unit. Volume densities are per millimetre.
- `sun_travel` is the direction the sunlight travels: pointing down, away from the sun.
- Every builder takes an optional dictionary that replaces only the numbers you name. Everything else keeps its default.

## Putting it on a scene

```python
import sys
sys.path.insert(0, '<skill>/scripts')
import pool_sunlight as ps

light = ps.load_light('/path/to/maps/demo-pool.json')        # written by make_light_map.py
sun_travel = (0.45, 0.65, -0.62)

floor.data.materials.append(ps.floor_light_material('Pool floor', light, sun_travel, tile_a, tile_b, grout))
wall.data.materials.append(ps.tile_material('Pool wall', 'XZ', wall_a, wall_b, wall_grout))
surface.data.materials.append(ps.water_surface_material('Water surface'))
body.data.materials.append(ps.water_body_material('Water body'))
ray_box.data.materials.append(ps.sun_ray_material('Sun rays', light, sun_travel))
ps.add_suns(collection, [floor, wall], sun_travel)
ps.setup_render(scene)
ps.setup_sky(scene)
```

The scene needs five things: a floor, the walls under water, a water surface, a closed box for the water body, and a second closed box for the sun rays. Keep the ray box about 5 mm inside the body box on every side, and keep the body box off the tiled faces. Where two volumes share a face, or a volume face lies on a surface, Cycles can skip one of them and the rays vanish in a band.

## One lookup for both effects

The map was made for a sun straight overhead. Its coordinates mean "the point where the ray entered the water surface".

Every shaded point, on the floor or in the water, slides up the refracted sun direction to the surface and reads the map there:

```
up     = the sun ray after refraction, pointing up
t      = (water_z - z) / up.z
entry  = (x + t * up.x, y + t * up.y)
uv     = (entry - domain origin) / domain size
```

So the floor pattern is the map shifted along the sun, and a sun ray is the same map value held constant along a slanted line. Both are read from one place, which is why a shaft always stands on a bright part of the floor and why the two stay together when the sun direction changes.

The map is never repeated (`EXTEND`), because a repeat reads as wallpaper. Keep the whole view inside the domain.

## The floor

```
L      = sharp map x 0.53 + soft map x 0.47
L      = 1 + (L - 1) x keep            keep falls from 1 to 0.35 between 1600 and 4500 mm from the camera
wash   = base + sum of broad Gaussians
colour = tile x (0.95 + 0.12 x L) x wash
       + warm colour x 3.8 x clamp((L - 1) / 10) ^ 1.5 x wash
```

| Key in `floor` | Default | What it does |
|---|---|---|
| `sharp`, `soft` | 0.53, 0.47 | The mix of the two maps. More `soft` makes the light paler and wider; more `sharp` makes it wiry. |
| `lo`, `mul` | 0.95, 0.12 | How much the pattern modulates the tile colour. With mean light 1 the tile keeps about its own brightness. |
| `warm_gain`, `warm_from`, `warm_range`, `warm_pow` | 3.8, 1.0, 10.0, 1.5 | The warm light added where rays gather. It rises smoothly from light = 1 and is not clamped at the top, so the tightest knots reach a warm-white centre. |
| `warm_rgb` | 1.0, 0.86, 0.66 | Colour of that added light. |
| `fade` | 1600, 4500, 0.35 | Distant floor is seen through more water, so its pattern eases back toward even light. `None` turns this off. |
| `wash` | base 0.75, no lobes | Where the sunlight lands. Each lobe is `[cx, cy, sigma_x, sigma_y, gain]` in map coordinates. Negative gain makes a quiet area. |

Every step is continuous. There is no threshold anywhere, so no hard edge can appear. Do not add one: a threshold on density was tried for the warm centre and gave hard-edged strokes.

The wash is what reads at thumbnail size. Put its lobes where the map's wide groups are (`method.md`), so the broad brightness and the fine light agree. Changing a lobe does not need a new map.

Tiles: `tiles` holds `size` 90, `grout` 1.6, `bump` 0.2 and `rough` 0.18. The tile and grout colours are arguments. Keep the grout visible but quiet; strong grout lines compete with the light.

## Keeping other things from drawing on the floor

The map is the only thing allowed to put a pattern on the tiles. Three things would otherwise add their own, and each is switched off on purpose.

- **The water surface.** `water_surface_material` is glass to camera and bounce rays, and a flat transparent pass (gain 1.15) to shadow rays. Without this, a rippled surface casts its own second, noisier pattern, or simply blocks the sun.
- **The sharp sun.** `add_suns` makes two suns and splits them with light linking. The sharp sun (0.6 degrees) lights everything except the floor and the underwater walls. Those are lit only by a wide sun (8 degrees) travelling along the refracted sun direction. A wide sun gives soft, enlarged shadows on the tiles, which is how a shadow looks through water, and no crisp edge to fight the map. Do not also give the wide sun a shadow-linking collection: in Cycles 5.2 that left the floor dark and speckled.
- **Path-traced caustics.** Off, both kinds. They are noisy and would double the pattern.

`setup_render` also turns the light tree off. With it on, the two linked suns sampled unevenly.

## The sun rays

```
density = fade(z) x max(soft map - 1, 0) ^ 1.6 x 0.8
fade(z) = smoothstep from 0 at 900 mm deep to 0.01 per mm at 25 mm deep, x exp(z / 420)
```

Only the brighter-than-average parts of the soft map make rays, and the power keeps the weak ones from joining into a haze. The rays are a scatter-only volume, lit by the sharp sun.

| Key in `rays` | Default | What it does |
|---|---|---|
| `density` | 0.01 | Peak density per millimetre. The main strength control. |
| `gain`, `pow` | 0.8, 1.6 | Strength, and how strongly bright areas are favoured. A higher power gives fewer, more separate rays. |
| `depth`, `top`, `falloff` | 900, 25, 420 | The rays are strongest just under the surface and thin on the way down. Set `depth` at or below the floor. |
| `rgb` | 0.14, 0.88, 1.0 | Scatter colour. Low red keeps the rays the colour of the water. |
| `anisotropy` | 0.0 | Leave at 0 unless the camera looks toward the sun. |
| `clear` | none | Ray-free zones, each `[cx, cy, cz, r0, r1, [sx, sy, sz]]`: no rays inside radius `r0`, full strength from `r1`, with the distance scaled per axis by the last item. |

Use a clear zone around a subject: a ray crossing a face or a body reads as a stripe painted on it. Use one around the camera too when the lens sits in open water: rays right in front of the lens read as fog, not as rays. The demo scene does both (`camera.ray_clear` and `subject.clear` in `assets/demo-scene.json`).

### The rays also shade

The rays are a scattering volume, so sunlight that has passed through a shaft arrives weaker and redder. It shows in three places:

- **On the lit floor.** Each bright patch sits under its own shaft, which tempers it. That is part of the look this recipe was settled with. It is also why a floor measures calmer with the rays on (see the patch numbers in [checks](checks.md)).
- **On a plain floor.** With the floor light off (`--show rays`) the shade is all the floor has, and it shows as soft grey smudges under the shafts.
- **On a subject.** A shaft between the subject and the sun leaves a darker, warmer blotch on it. With a zone centred on the demo ball and 230 mm of ray-free water around its centre, the ball came out blotched.

So the subject's clear zone has to hold more than the subject: the water between it and the sun, and the water between it and the lens. In the render the sharp sun's light is not bent at the surface (see Limits), so "toward the sun" means the sun's direction above water. The demo moves the zone 200 mm that way (`subject.clear_lift`) and clears 400 mm around the new centre, which left the ball clean. For a deep subject, put two or three zones along the path.

Do not try to switch the shade off with a Light Path node on the density (`Is Shadow Ray`). It was tried here: a test picture that renders in three minutes without the node had not finished after 28 minutes with it.

Rays show best against something darker than they are, such as a deep-coloured wall or the far water. Against a pale sunlit floor they are faint. That is a matter of where the camera looks, and it is the same under real water.

## The water

`water_body_material` is absorption for the blue-green depth colour plus a little even scatter for haze. Defaults: absorption 0.0026 per mm with colour (0.5, 0.83, 0.92), scatter 0.00016 per mm with colour (0.08, 0.85, 1.0).

**The density is a look choice that depends on how much water lies between the lens and the subject.** The defaults suit a close subject one to two metres away. The demo looks down three to five metres of open water, where the defaults give an even teal haze that hides both effects, so its scene file lowers them to 0.0017 and 0.00006. Start from the distance: thin the water until the far floor still shows its light, then bring the rays back up with `rays.density` if needed. Lower the water, not the rays, when a picture is hazy.

## Lights, sky and tone

| Setting | Default |
|---|---|
| Sharp sun | strength 6.5, colour (1.0, 0.78, 0.55), angle 0.6 degrees |
| Wide floor sun | the sharp sun's strength x 0.9, same colour, angle 8 degrees, travelling along the refracted sun direction (`floor_sun.travel` overrides) |
| Sky | gradient from (0.55, 0.7, 0.92) at the horizon to (0.24, 0.42, 0.8), strength 0.42 |
| Tone | AgX, "Medium High Contrast" look, exposure 0.05, white balance 7800 K |
| Cycles | 320 samples, adaptive 0.03, OpenImageDenoise, 16 bounces (diffuse 3, glossy 6, transmission 12, volume 1, transparent 64), indirect clamp 8, caustics off, light tree off |

This is a warm, late-afternoon sun. For midday, whiten the sun colour and drop the white balance toward 6500 K; the floor and ray numbers do not need to change.

## Limits

- The floor must be flat and level for the placement tool (`screen_to_lookup.py`) to be exact. The materials themselves work on steps and slopes, because every point does its own lookup.
- The look of the water surface seen from below (its ripples, its mirror of the floor) is not part of this recipe. The demo's surface is a flat sheet and the demo camera does not look at it.
- Shadow rays pass straight through the surface without bending, while the floor light and the rays follow the refracted direction. A subject's shadow therefore falls along the unrefracted sun. The wide floor sun hides most of this; it is a known, accepted inconsistency.
- The defaults were settled on one pool about 700 mm deep. Deeper water spreads and softens the light: remake the map with the new `depth` (`method.md`) and lengthen `rays.depth` and `rays.falloff` in proportion.

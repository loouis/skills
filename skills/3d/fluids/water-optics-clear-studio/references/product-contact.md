# Curved contact and a readable reflection

The selected reference direction combines a front waterline below the side joins, a narrow raised rim, small uneven local ripples, warped reflected type close to contact and quiet open water. A reflection should read as light on water, not another solid product attached below the first.

The bundled `assets/contact_field.py` is a self-contained numerical height field, with exact settings in `assets/contact-settings.json`. It preserves the selected formula, including broad base waves, irregular optical coordinates and shared near-contact extent. It does not load a product, create a complete studio or implement a fluid solver. The public demo shows separate optical benches; it does not claim a reproduced product shot.

## Coordinate and geometry contract

Coordinates are metres: X lateral, Z up, negative Y toward the camera. The original fixed camera was(.016,−3.2,.29),356mm. Contact distance is based on an 18° Y-tilted reference cylinder translated to Z−.010. Its bottom radius profile uses 16 samples of the cubic Bezier control points[(.0245,0),(.0255,.003),(.0288,.006),(.029,.012)]. Replace this distance function to match the receiving product and revalidate the intersection. The formula is an authored local approximation, not a general signed distance or measured wetting angle.

`evaluate(x,y,t,settings,quiet=False)` accepts NumPy scalars/arrays. Time is seconds, with reference phase at47/24. Sample a sufficiently dense top grid; create outward-facing sides and a bottom outside the camera footprint. The historical pool used913×1812 top vertices. Keep the bottom fixed when animating. Smooth normals cannot repair inadequate geometry sampling. Test the whole camera footprint, including reflection/refraction rays.

## Selected parameters

| Control | Value and purpose |
| --- | --- |
| Far pool level | +7mm |
| Relative side join | +.4mm |
| Front depth term | 2.4mm, approximately2mm below far pool at centre |
| Return length | 9mm sides →48mm front, smoothly varying with facing angle |
| Lateral bound | full within32mm of X=.007; quintic fade over next34mm |
| Local crest | .14mm amplitude,8mm offset,5mm width |
| Local ripple | .08mm amplitude,34mm wavelength,speed1.4,asymmetry.38 |
| Near optical boost | parameter3 gives maximum4×; not3× |
| Near coordinate shift |10mm, smoothly localized near Y=−70mm |
| Extra waves |25/10µm amplitudes,63/137mm wavelengths,15/9mm smooth phase warps |
| Extra envelope |74mm lateral width,600mm longitudinal span,centre−430mm |
| Shared near field |same optical field through100mm from contact; quiet branch fades it over next80mm |
| Fine repeated ripple |disabled, amplitude0 |
| Effective pool roughness |SMOOTHERSTEP on −worldY:40…950mm maps.025….085 |

Do not substitute the unlinked roughness socket default. The copied pool material uses a linked map; other water objects keep their materials. Config keys `attached_contact_height` and `capillary_length` are legacy context: the new `attached_contact()` uses the depth/return values above.

## Three-plate composition, when requested

The source treatment combines three matching scene-linear plates:

1. **Distorted beauty:** product visible, full optical field.
2. **Distorted no-product-reflection:** same direct product, camera, materials and field; selected product meshes excluded from glossy rays.
3. **Quiet:** same no-product-reflection setup, with the extra field fading outside the shared contact neighbourhood.

Compose `quiet + gain(row) × (beauty − no-product-reflection)` before AgX. Gain is1 through top-origin normalized row.725, then quintic smoothstep to.75 at row.840, remaining.75 below. It changes reflected contribution, not pixel coordinates. This is fixed-camera art direction, not a physical Fresnel model. Glossy exclusion is a renderer visibility control; verify exactly which objects participate and check direct visibility in every plate.

Geometry agreement near the join is necessary but not sufficient: reflected rays can reach a more distant region. Inspect native beauty versus composition for seams. A uniform.75 contribution made an artificial contact band even with shared geometry; keeping1 near the join removed most of it without strengthening the whole lower reflection.

When building a Blender float mask, set its Non-Color colour space **before** assigning pixels, then update and pack it. Setting colour space afterwards reset one tested buffer to black. Reopen the compositor and verify values as well as rendered output. Keep calculations scene-linear; never subtract display-transformed JPEGs.

## What the iterations established

- A narrow3.2mm trough existed in3D but was largely hidden by nearer water. Broader returns exposed it while creating wide dark shoulders.
- Raising immersion brought the reflected type nearer contact but did not create the needed downward curve.
- A full-resolution pass revealed that a5mm relative dip/120mm front return was too broad. The selected2mm/48mm version retained a curve and narrowed the rim.
- Increasing near-wave strength to9× made regular parallel bands.4× plus a modest10mm local phase shift was better.
- The final1600×2000 still received a scoped9.0/10 reviewer assessment, with natural ripple irregularity weakest at8.8. The user then positively received the small ripples and water appearance. Keep this as an appearance baseline; no new full motion or equilibrium solve was approved by that feedback.

Use these values as an exact worked example, not universal distances or automatic9/10 settings. Slight ripple orderliness, sampling/denoising limits and studio/reference differences remain.

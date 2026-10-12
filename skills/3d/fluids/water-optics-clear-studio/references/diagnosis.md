# Diagnose the cause before changing the look

| Visible problem | Useful matched control | Demonstrated lesson |
| --- | --- | --- |
| Shelf-like reflection or squared letter | same camera at higher native pixel density; normals control; lower only wave height | Steps survived density/normal controls but diminished with lower wave amplitude. Inspect slope/stretch and directional wave spacing before editing the glyph. |
| Fine horizontal bands across quiet water | remove only the small repeated wave term; inspect raw and denoised | A10µm/45mm term visibly striped open water at grazing view. Its removal calmed water but made type too mirror-like. Retain irregular localized curvature rather than restoring the full fine pattern. |
| Two solid products apparently joined | compare native reflection contribution, near contact and lower reflection together | Weak water contact plus overly strong continuous reflection can destroy the water reading. Restore attached curvature/local waves and control contribution; do not conceal the join with a broad band. |
| Flat visible join despite a deep mesh dip | trace actual intersection and inspect foreground occlusion at the camera angle | A projected mesh-contact curve is not proof of visible curvature. Test front reach, side return and immersion independently. |
| Thin seam after composition | native beauty versus composed image at the same pixel density | Ensure shared geometry across the full relevant optical path and inspect contribution gain at the product boundary. |
| Broken optics on one backend | same scene and settings on another backend | One product-pool case was restored by CPU. Do not universally blame GPUs, normals or materials without a matched test. |
| Hard rectangle through transparent water | enlarge/feather the reflection source and inspect its margins | Sources outside the direct crop still appear through reflective/refractive rays. Camera invisibility alone does not remove them from water. |
| Faceted print on a cylinder | compare surface geometry, shading normals and artwork offsets separately | Preserve the approved letterform; use clean curved shading and sufficient geometric sampling. |

Preserve the untouched camera/product/studio for diagnostic comparisons. Change one likely cause when possible. Copy a material before a pool-only change, verify the object's effective material (including object-level overrides), and check whether the changed light/object is actually active. A node edit on an overridden material or a hidden light can produce no visible change.

Before diagnostic renders, redirect **all** compositor File Outputs as well as the beauty path. Never overwrite earlier raw evidence. Native crops should be newly rendered or shown at actual pixel scale; enlarged previews are not additional detail. Retain failed controls with their cause and supersede a former readiness score when user feedback exposes a missed defect.

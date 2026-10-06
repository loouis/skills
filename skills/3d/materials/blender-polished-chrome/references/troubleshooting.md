# Troubleshooting

| Visible defect | Controlled diagnostic | Useful next change |
| --- | --- | --- |
| Satin-looking grey column despite sharp highlights | Toggle only floor glossy visibility for one draft, then restore it | Broad feathered floor card; retain existing upper diffusion |
| Whole product too dark after that toggle | Restore floor glossy visibility and inspect all views | Reshape reflected tones; do not keep a rejected diagnostic as final |
| Soft reflections everywhere | Compare lower roughness with fixed lighting; inspect normal paths | Reduce excessive roughness/bump; inspect sampling and denoising |
| Hard rectangle across curved metal | Hide one panel at a time to identify the source | Broader panel, softer opacity/tone ramp, changed orientation |
| Dark band ends abruptly down a cylinder | Inspect the entire body while moving the card | Move/extend/rotate the card; try a floor-aligned source instead of a finite vertical flag |
| Front becomes black when diffusion is removed | Restore the panel at the original exposure | Keep useful broad upper lighting and tune its gradient |
| Washed-out shape or vanished side ridge | Reduce fill temporarily; inspect unclipped highlight transitions | Lower radiance or move the panel, retaining modeled ridges |
| Faceted raised profile or silhouette | Inspect wireframe, bevels and evaluated normals | Separate geometry revision within authorised scope |
| Fuzzy small detail | Inspect a native render at 1:1, with denoising comparison if needed | Render enough actual pixels/samples; avoid upscaling, blur and aggressive filtering |
| Floating object or patterned backdrop shadow | Check contact and card ray visibility in the full frame | Keep the object's shadow; correct card placement or documented direct-shadow exclusion |

Avoid fixing every defect with lower roughness. A polished surface faithfully reveals an unsuitable environment and any mesh/normal problems.

## Blender scripting pitfalls

- When changing visibility during collection traversal, use `for obj in list(collection.all_objects): ...`; mutating visibility can invalidate a live iterator.
- Before opening another `.blend`, recursively convert RNA-backed vectors, socket values and matrices into plain Python numbers/lists/dicts. Old RNA owners become invalid after the file switch.
- Keep a separate saved revision for each retained result and refuse accidental overwrites. Do not resave an original merely to generate a matching baseline render.
- Choose CPU or a supported Cycles device for the current host. A Metal shader-cache crash on one host was avoided with session-only `kernel_optimization_level='INTERSECT'`; this is a targeted troubleshooting option if that preference exists, not a required render setting or a global preference change. Do not prescribe Metal on other hosts.

When a renderer fails, record the actual version/device/error and retry with a supported conservative device or the documented version-specific workaround. Preserve visual settings while diagnosing execution problems; do not silently lower quality and call the result equivalent.

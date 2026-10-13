# Adapting suspended water to an actual product

## Audit all renderable product geometry

A preserved product contained a casting stored as a native surface. The evaluated scene displayed it as a mesh, while a raw `type == MESH` filter omitted it. The first audit therefore counted one fewer product part. Include evaluated surface/curve geometry as appropriate, alongside original meshes, transforms, modifiers, material graphs, linked libraries and supplied artwork. Settle the view layer before comparing transforms.

This finding establishes audit coverage. It does not demonstrate collision, good water placement or visual realism. Technical checks must remain separate from the beauty score.

## Begin the transfer with an explicit placement test

Preserve the actual selected product and its finish. Reuse the reviewed water as a separate collection, recording its scale, orientation and offset in physical units. Plan a bounded output batch and reconstruct routine variants from one pinned baseline in memory. Keep each pass's setup source frozen so later edits do not invalidate its recipe.

Review whether the whole water envelope fits the frame, whether the head/outlet and identifying features stay readable, and whether the apparent wrap has convincing depth. A bottle-oriented sheet is a starting asset, not evidence that it fits another product. Its original lighting and still score do not transfer automatically. Further optical/contact findings should be added here only after the new render is inspected.

## Settle imported transforms before applying placement

A new scene rendered repeated product ghosts and large dark blocks. Native ray inspection found a nominal detached drop had become a huge glass sphere surrounding the product. There were no duplicate water instances or parent transforms. The placement loop had read `matrix_world` immediately after appending/linking the collection, before dependency evaluation; small source scales and positions were not yet represented in those matrices.

After linking, call `bpy.context.view_layer.update()` **before** taking a snapshot of source transforms or multiplying by the new placement matrix. Compare the imported collection's evaluated bounds and object transforms to independent source evidence first. Then apply placement, update again and compare against the intended result, allowing only a declared floating-point tolerance. A later check against targets computed from the same unsettled state can pass while the image is completely wrong.

The native bounds diagnosis and corrected import preflight establish this setup error. The subsequent full/raw composition probe removes the ghosting and background blocks; this recovery does not establish a successful splash composition. Do not blame the render backend on appearance alone, and do not report an interrupted device test as evidence of a backend discrepancy.

## Protect the product while revealing water

A ray-guided diffuser improved water folds and droplets but washed out the product display and tray. Water-only receiver linking restored the display; the excluded mesh source still introduced a dark patch in the tray. Keep those as separate observations: lighting contribution and physical source occlusion are different mechanisms. A following linked native area-light control restored the tray and retained the dark display while revealing the broad water folds. Its uniform radiance differed from the feathered mesh profile, so this was not an identical-radiance comparison. The remaining broad white patches still required refinement. Test a linked native area light when an excluded mesh source still harms another reflection. Verify the whole product after each control and keep receiver collections uninstanced so they do not duplicate the water.

A later floating composition exposed a broad white patch in the water with the uniform area source. Changing only its transmission factor produced no useful visual change. Returning to the feathered mesh with explicit ray visibility recovered the clear centre; source size, strength, spatial profile and visibility changed together, so the responsible factor was not isolated. The earlier accessory occlusion no longer appeared once that accessory was intentionally excluded. Choose the source for the current composition and verify its actual effect; neither source type nor a parameter name is a universal fix.

A geometric first-hit normal probe located a candidate strip, but a glossy-visible/transmission-invisible source did not reveal the intended central highlight. Changing only the mesh source to be visible to transmission rays exposed a broad bright patch. Object ray visibility affected this nested-water path, while an earlier area-light transmission-factor control did not visibly help. Keep these controls distinct. Probe directions are candidates; judge the traced result and narrow or dim an oversized source rather than treating every bright patch as a material defect.

Also check the new product's actual envelope. A visually plausible borrowed wrap contained water vertices deep inside a cylindrical column. An old bottle-oriented asset and an unchanged product audit cannot establish new contact. Any authored cavity/clearance correction must be measured after evaluation and reviewed in the full still; it is not a solved impact or motion result.

## Reject clearance fixes that destroy the splash

An exact cylinder difference on a previously offset frozen-fluid surface removed most of the connected membrane and both plumes. Evaluated vertex/edge clearance passed because the damaged geometry was gone. A large unexpected vertex-count reduction and minimum clearance well outside the cutter were warning signs. The experiment does not isolate winding, self-overlap or Boolean classification as the cause. Preserve the original source, compare the complete envelope and topology statistics, and reject a technically clear but visually broken result. A topology-preserving deformation also needs face-level clearance and fold/thickness review; do not assume that moving vertices outside a collider makes every face safe.

## Bound deformation by the intended feature

A field intended to widen the lower trail used height alone. It also caught low fragments at both main-sheet margins and stretched them into long thin sails. A closer floating composition made the error conspicuous. Constrain a correction by distance to the intended feature as well as height, preserve the full-source topology/envelope record, and inspect both side margins. The following height-and-distance field, with bounded native smoothing, widened the intended trail without the lateral-sail regression and retained topology. Repeated curls remained visible, so this establishes the benefit of spatial support rather than a universal finished preset.

A stronger local smoothing control softened fine detail without removing broad repeated bends. A following wider, polynomial-centreline-faired trail introduced stretched transition ridges and a stiffer strip; that combined change was rejected. Treat mean curvature, cross-section, local detail and width as different controls. Preserve the strongest prior branch when a technically valid deformation weakens the liquid shape.


When excluding a product accessory, materialize `list(collection.all_objects)` before mutating visibility. A live traversal in the tested scene changed only its first matching object; a separate snapshot correctly changed all intended parts. Verify the final visible assembly and retain the original geometry.

## Recheck thin contours when changing the background

A matched dark-to-white backdrop comparison retained the product and water geometry but weakened the upper plumes, detached beads and thin outer margin. Clear transmission through a pale field did not compensate for the lost contour contrast. Compare both the broad membrane and the finest silhouette features; a white background is not automatically clearer. Backdrop changes also leave repeated geometric curls untouched. Keep background preference separate from whether the water shape is convincing.

## Compare inherited thickness before blaming the normals

A transferred fluid membrane showed a heavy glass-like rim and angular tonal patches. The original pre-offset source was available. Reapplying its bounded smoothing and 1.8mm normal offset reproduced the selected source vertices exactly; only then was the offset reduced to0.3mm for a matched native comparison. The rim became thinner, but the patches remained in raw and denoised pixels. This proves a limited thickness effect, not a complete repair or a normal/backend diagnosis. Preserve the old treatment, verify reconstruction and inspect the local shape before introducing another filter. Smooth polygon flags and subdivision alone do not establish optical quality.

## Separate airborne drops from attached wetness

When a polished cylindrical product needs attached beads, a small closed cap with a cylinder-conforming underside can preserve its original finish. In the tested still, each cap had a nominal5µm clearance, shared rim vertices and two incident faces per edge; evaluated face/edge clearance and single instances were checked separately from the large splash. This is an authored wetness cue, not a wetting or drainage solve. Keep their object/receiver set separate so adding beads does not invalidate the imported splash count. Check the final adapted geometry before attributing an apparently flat drop to reflected light.

## Preserve detached particles through envelope changes

An independent source audit showed rounded drops, but the adapted image showed flat ovals. The plume-spreading field had been applied pointwise to every vertex, stretching one detached drop by more than3× in a principal dimension. Move each detached particle as a rigid body through an envelope-placement field unless its deformation is intentional; keep continuous deformation on the connected sheet. In the tested correction, using the average field displacement per particle retained the desired distribution, recovered rounded native silhouettes and preserved114 final particle shapes to a relative principal-scale tolerance of1e-4 after accounting for uniform placement scale. Audit the final geometry, not just the imported source. This check does not validate trajectories or aerodynamic deformation.

## Verify modifier support after applying earlier modifiers

A second smoothing operation silently received an empty vertex-group name from a retained RNA group wrapper after the first modifier was applied. It smoothed the entire connected surface and softened the plumes. The first filter had exact weights and zero motion outside its mask; the second moved every intended zero-weight vertex. Re-resolving the group by its stored string name fixed the test: the same zero-weight vertices remained exactly unchanged through both operations. Store stable identifiers, look up the current item after destructive operators, assert the modifier binding and measure displacement outside the intended support. A group assignment in source code is not proof that the evaluated operation stayed local.

## Distinguish a tonal patch from first-surface faceting

A patchy clear-water region appeared almost identically on CPU and Metal. Higher transmission/total/glossy limits changed nearby bright detail but retained the patch structure. An opaque shading-normal diagnostic showed smooth transitions across the visible region, with no custom normals or sharp edges. These controls reject a backend-only explanation and do not support literal first-surface faceting; they do not isolate later refracted surfaces or source visibility. Inspect those optical paths before adding more geometry smoothing. An appended water collection also does not bring its source scene's global integrator settings: record and compare them explicitly.

A matched zero-glossy-filter control produced almost no visible change in the same water window, so disabling filtering was not a demonstrated repair. Sampled straight camera rays through the evaluated water had alternating entry/exit face orientations; this did not expose a reversed boundary in those samples. Straight-ray checks do not follow refracted paths and cannot prove the whole mesh is free of intersections. Keep such negative controls as limits on a diagnosis, not evidence that every optical path is correct.

# Tested failures and next controls

| Visible failure | Evidence-supported next step | Limit of the inference |
| --- | --- | --- |
| Corrugated annular collar | Replace the repeated radial form with broad connected folds; separate centre and margins | Fine detail and thickness alone did not repair composition |
| Spikes at cut rims | Inspect evaluated offsets, normals and narrow cuts; retain a no-even-offset control | The improved pass changed both sheet construction and offsets, so the sole cause was not isolated |
| Frozen, orderly deep folds | Try short liquid relaxation from the intended envelope | More depth was a regression in the source study |
| Organic edges but oversized fan | Correct the initial envelope and launch before adding render density | Multiple solver settings changed together; no single-parameter cause was established |
| Narrowed sail or needle tips | Avoid strong anisotropic sculpting of a frozen frame; rebuild the source silhouette | Voxel union filled the centre but created bar-like reflections and spikes |
| Fine horizontal combing | Inspect the native raw surface, then test bounded geometric filtering | Denoising was not the only source of these striations |
| Weak silver centre despite front fill | Inspect actual reflected-ray directions and place diffusion there | Ray samples can hit hidden sources; verify object identity |
| Broad bright bars | Inspect source boundaries and sheet curvature separately | Roughness can blur the failure without fixing it |
| Fine grain or disappearing droplets | Compare same-run raw and denoised native details; improve sampling where needed | More pixels do not guarantee convergence or preserve every denoised strand |

Two dense-mesh attempts grew to roughly 22–34 GB while an operator-driven dependency update evaluated subdivision. Snapshotting normals alone did not resolve the problem. The combined workaround deferred subdivision, batched arrays, used 128 weight levels and restored subdivision last. Do not present this as an isolated proof of one memory cause.

An initial collection audit falsely failed because appended transforms had not been evaluated and it rejected an unused library record. Update the view layer, compare evaluated world transforms, then inspect the objects and mesh/material/image dependencies actually used. A remaining unused library record alone is not proof that the exported water requires it.

Keep failures and their settings in the receiving project. A failure may support a diagnostic rule without becoming a successful recipe. Withdraw readiness claims when later user feedback reveals an overlooked visible defect; preserve the historical outputs and record the narrower current conclusion.


### Closed edges can still contain an inverted thin region

A dark square-looking root patch had zero non-manifold edges and zero inconsistent oriented edges, yet three of seven camera rays met an outward boundary with an exit-facing normal before an entry-facing one. This is evidence of a locally inverted/overlapping geometric boundary, not proof of an ordinary face-winding error. A bounded0.9mm outward normal offset restored entry/exit order on all seven sampled rays; same-run clean/raw images still showed a stiff broad fold. Topological closure and corrected ray ordering therefore do not by themselves establish a good-looking splash. Test the geometric thickness separately from contour curvature and reflected source placement. These are straight diagnostic rays, not refracted light paths or an exhaustive self-intersection audit; keep the finding scoped to the sampled region. Preserve coordinates outside the correction support and validate that new changes do not cross the product.

A later probe outside those seven rays found another reversed first crossing. A wider repair gave84root rays (62hits), no reversed first crossing, but four deeper non-alternating sequences. Extend sampling beyond the first successful points and distinguish a corrected entry boundary from complete volume validation. Whole-mesh and isolated-trail exact self-intersection Boolean controls both exceeded a28GB process-memory guard. A fine voxel rebuild of only the616856-vertex trail completed at16.34GB observedRSS and produced825552vertices; native contour and clean/raw review retained its shape with slightly smoother fine reflections. This made the boundary operation feasible but did not resolve the remaining root silhouette or earn a higher visual score. The user-visible defect remains the acceptance criterion.


### Investigate preservation failures before relaxing them

A local Boolean notch removed eight protected vertices while every remaining exterior coordinate stayed exact. The deleted points were up to0.393mm from the resulting surface, so a coplanar/roundoff exception was rejected. Incidence checks showed they formed a complete8vertex/6face closed disconnected piece. Restoring that exact piece with BMesh recovered the protected coordinates and edge closure at the notch stage; low-level enlargement of an evaluated mesh had crashed and was replaced. Inspect lost/added coordinates, surface distance and connectivity before changing a preservation contract. Restore only verified complete geometry, retain a strict post-check and state which stage the guarantee covers. A subsequent declared remesh/union needs its own scope; do not silently extend an intermediate exactness claim to the final asset.

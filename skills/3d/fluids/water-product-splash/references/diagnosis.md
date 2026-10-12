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

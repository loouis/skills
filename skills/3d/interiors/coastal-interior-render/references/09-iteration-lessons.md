# Iteration history distilled into repeatable decisions

This is the complete sequence of major problem families and decisions, not a transcript or a claim that every experiment succeeded. Source revision numbers are retained only to distinguish evidence. The original production files are not part of this public package.

| Stage | What happened | Rule to carry forward |
| --- | --- | --- |
| Reference and plan study | Marketing imagery established a palette; 17 plans clarified practical use | Study pixels and plans separately; distinguish observed, published and proposed |
| AI concepts v01–v12 | Attractive concepts drifted on stool recess and geometry; a dimensioned blockout helped | A measured planning model does not certify generated pixels; preserve concept versus construction distinction |
| Direct reconstruction | User requested editable geometry matching the concept | Render actual Blender geometry; do not replace it with AI retouching |
| Early furniture | Basic stools/sofa and wrong grain weakened the room | Product references, silhouette, member UVs and support joints come before microscopic texture |
| R25 review | User assessed it nearer 8 despite earlier generous scoring | Reference comparison governs; model complexity is not a quality score |
| Sink/stone/hardware | Tap on wrong side, incomplete bowl, large gaps, inconsistent slab thickness | Define cook side; inspect overhead/working side; measure all joints and usable pulls |
| Multipart imports | Plant soil shifted independently; mixed source units appeared | Capture every original world transform before group placement; verify whole assemblies |
| R40–R46 | Area sources appeared through glazing, appliance reflections blew out, cushion grooves looked repeated | Check source corners/rays; inspect geometry and reflection separately; no arbitrary wrinkles |
| R47–R50 | Upholstery gained weave but broad compression and seam quality lagged | Review form, tailoring, texture and light independently; include welts in clearance |
| R51–R62 | Throw needed longer side/front drape, folds, smaller cushion and better fringe | Whole drape/contact first, then pattern/yarn; full hem and overhead cameras required |
| R63–R65 | Sea looked at floor level; rail returns and plate coverage were missing | Terrace, horizon, shoreline depth and wave scale together; check every saved camera |
| R66–R76 | Selected Sophie Lite reconstruction exposed arm tips, carrier, cushion support and seam ends | Match the correct low variant and inspect orthographic/rear/tailoring views; keep product attribution honest |
| R77–R79 | Sofa lifted 40 mm, patterns compared; local cloth snapping made jagged folds | Move all furniture parts, preserve rug support and use continuous drape adjustment |
| R80–R96 | More folds produced stiff loops, crossed rolls and crushed cloth | Preserve stable gravity envelope; intentional overlap requires separated surfaces |
| R94/R95 | Sideways rolls looked plausible in main views but intersected | Confirm coarse flags at full resolution; a hero cannot clear geometry |
| R97–R106 | Improved weave and fine fringe; rest-shape experiments failed | Inspect frame-one bounds and keep rejected bakes out; more fibres do not fix poor joins |
| R106 reopened | Root proximity passed but flat-cut bundles under a cord looked detached | Require continuous woven lead-ins and visual construction, not just distance |
| R107/R108 | Better continuity became comb-like or sparse strands | Preserve user-preferred fullness while fixing attachment |
| R109/R110 | Long triangular gathers rejected; short gathered roots and soft full skirts selected | Secure the root, maintain shared bends and unequal ends; target remained open |
| R111/R112 | Pale hob misread as absent; plant obstructed foreground | Diagnose ceiling reflection before changing material; check object silhouettes |
| R113 | Heavy bevels made a bonded stone joint read open | Separate exposed arris easing from mitre easing |
| R114/R115 | Selector direction and raised-looking TFT failed close review | Camera-projected left/right and closed coplanar hob; show all four corners |
| R116–R118 | Stronger/oblique sun did not solve appliance light and created wall patches | Keep actual overhang; test bounded fill and diagnose the cause |
| R119 | Faceted tap, pinched basin fall and floating stems found overhead | Functional detail views catch faults beyond hero composition |
| R120 | Appliance fill caused unnatural wall strip | Matched sun-off/fill-off/glossy-off tests isolated diffuse spill; 7 W→0.5 W repair |
| R121/R122 | Materials separated better, but nubuck mottling was too strong | Calm broad variation; keep fine nap distinct from low-frequency stains |
| Sun 8/16 control | 16 lost pale detail; 8 retained useful shape | Relative lighting/exposure tests beat copying a brighter number |
| R123/R124 | Marble014 looked blotchy; quiet travertine restored | More dramatic stone is not automatically more luxurious |
| R124/R125 camera | Added camera obstructed by storage; wider correction cut the table | Keep the complete architectural composition; don't conceal missing space |
| R125/R126 rug | Darker rug exposed coarse weave; four fine tiles created seams | Use continuous global texture/geometry and test at native detail scale |
| R127 | Fine continuous rug and balanced material/light direction selected | Independent curtain/rug gates before excluding them from preservation tests |
| R128 | Lower albedo and small veneer variation gave marginal gains | Reject later versions when core tailoring/highlight faults remain; keep prior selection |

## Specific anti-patterns

- Do not silently restore old geometry because an old build script is convenient. Identify the selected dependency chain before running builders.
- Do not inherit a previous score when the criterion changed. User feedback can correctly overturn a 9.8.
- Do not use nearby contact as proof of a joint. It failed both furniture support and fringe attachment.
- Do not hide errors with cloth, a tighter camera, darker materials, a smooth piping strip, reduced resolution or a painted highlight.
- Do not broadly exclude “soft furnishings” from regression testing. Audit exact changed objects, their anchors and contact first.
- Do not use a shader-name lookup without checking the actual saved scene; a late material rename can abort a batch.
- Do not launch a render batch with unchecked camera strings. A typo once failed after many completed images while the process code was misleading.
- Do not pass relative script paths in a fragile GPU launch. A prior Metal compilation launch failed; an absolute-path retry succeeded. Preserve logs rather than claiming a universal cause.

## Current boundary of evidence

The selected source image improved substantially but did not equal the benchmark. Uniform veneer, bright pale surfaces, furniture tailoring and some arranged fold/fringe rhythm remained visible. Whole room 9.3/kitchen 9.4/throw 9.5/stool 9.3 are scoped historical assistant judgements, not transferable scores. The public demo demonstrates a portable procedure only.

## Keep learning during use

After a new user correction, add the issue, diagnostic control, actual fix, regression checks and result to the receiving project's ledger. Promote only repeatable general lessons to this skill. Keep private images, paths, client details and failed scene files in that project. Record unresolved experiments as unresolved; do not rewrite the history as a success story.

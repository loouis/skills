# STATUS

_Updated 2026-10-06._

## Completed

- 2026-10-06: published `logo-mask-motion` (`skills/motion/logo/`, the first skill in the `motion` group) and extended it with the open-line case from a second build, a hexagonal mark with six blades between two rings: lines extended along their tangents under the rings, masks cut from the front stroke, rings that grow with their weight held, threading, draw-on gated by the junction, and an in-page landing check. Its demo gained a ring-and-spokes section (turn, grow, thread). `vector-masking` received the same material in its own structure (SKILL.md, `masking-method.md`, `tool-notes.md`). Validated and galleries rebuilt.
- Renamed the masking skill to `vector-masking` under `skills/ui/masking/` following the clarification that its purpose is teaching vector mask construction. The entrypoint now leads with whole shapes, occluding silhouettes, joins and gaps; motion-specific steps are conditional on animation being requested. Updated metadata, prompts, repository guidance, links and preview labels.
- Packaged the full supplied construction method and SVG, After Effects / Lottie and Figma implementation notes. Preserved constant strokes, flush travel, landing-only gap growth, hidden geometry, chained occluders, symmetry joins and exact artwork handover for animated masking.
- Added an original three-panel SVG demo with two final-gap variants, forward/reverse playback, frame scrubbing, phase jumps, mask inspection, static-source comparison and reduced motion. Includes a portable frame-export/check script, recreation prompts and a 1280 × 720 preview. No private source artwork, names or paths are packaged.
- Validation: skill-creator and all 17 repository skill checks pass. The naming correction leaves demo geometry and runtime unchanged. Prior Chromium checks at 600 × 420 show zero changed pixels for closed/front-only and final masked/original comparisons in both gap variants; 152 sampled poses show no foreground-interior leaks or tested travel gaps. Exported and inspected 76 frames, a contact sheet, mask view and 390 px mobile layout. Forward/reverse playback, comparison, keyboard scrubbing and reduced motion passed with no browser errors. Local links and public hygiene remain checked.
- Refreshed library indexes and galleries. Added vector-masking conventions and its verification command to `AGENTS.md`; `CLAUDE.md` continues to import it.
- Existing library: nine generated gooey-section skills, six self-contained GSAP page-transition skills and `blender-polished-chrome`. Prior transition parity/lifecycle/browser checks and Blender 5.2.1 helper/render/preservation checks passed. Original generic Blender renders remain the material demo assets.

## Current

- Two skills now teach one masking method in different voices: `vector-masking` (construction first) and `logo-mask-motion` (motion first). They were written in separate sessions from the same source. Keep them in step until Louis decides whether to fold one into the other.
- This public repository is `loouis/skills`. The library contains 17 skills in 4 categories; verify the active checkout's remote before changes.
- Vector mask publication is authorised. The web study covers stationary geometric occluders; organic reconstructions, moving-front chains and tapered root gaps are documented methods, not demonstrated by this fixture. After Effects, Lottie, Figma and physical-device behavior remain unverified.
- The expanding scroll panel remains a prototype under `prototypes/expanding-scroll-panel/`, excluded from installation and generated skill lists. Its background and content stay siblings.
- Gooey skills remain generated from the private labs source; see `AGENTS.md` before rebuilding. Page-transition shared cores remain identical except for defaults; “Suite” provisionally aliases Tidal sweep.

## Decisions

- Create groups/categories with their first skill, under `skills/<group>/<category>/<skill-name>/`. Classify vector masking by its construction technique; animation is an application of the method. Use original generic artwork in public demos and keep private source dependencies out of packages.
- Keep one skill per commit and publish when requested. Publishing does not require app-wide installation or website deployment.
- Preserve visible vector curves exactly, including arc commands in the demo; hidden continuations must remain long enough to cover overshoot. Renderer-specific mask behavior and export support need explicit checks.

## Next

- Apply the vector method to future artwork and adjust from observed defects, checking actual renderer output at joins and handover.
- Package the expanding panel controller when requested. Continue transition testing in receiving sites and material testing on other Blender versions.

## Blockers

- None.

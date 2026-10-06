# STATUS

_Updated 2026-10-06._

## Completed

- Added `blender-polished-chrome` under `skills/3d/materials/`, introducing the **3D** group and **3D Materials** category. The skill separates metal identity/reflectance, finish, reflections and geometry; includes detailed recipes, troubleshooting and preservation checks; and packages an optional feathered reflection-card helper.
- Created an original generic cylinder/ring demo with three actual Blender renders: satin, lower roughness, and polish with floor reflection control. Includes a portable generator, independent saved-scene verification, native JPEG downloads, accessible pointer/keyboard comparison, recreation prompt and 1280 × 720 preview. No source-project assets or scenes are published.
- New-skill validation: skill-creator and all 16 repository skill checks pass. Blender 5.2.1 helper tests cover geometry/UVs/orientation, graph/ray visibility, preservation, invalid inputs and save/reopen. Demo runs on Metal and CPU; final 1600 × 1200 PNGs are verified 16-bit, native JPEGs decode, and all three saved revisions preserve geometry/evaluated normals, camera/exposure/look and steel reflectance. Export code explicitly restores PNG depth after JPEG export.
- Browser validation: desktop 1280 × 720 and narrow mobile layouts; reveal Home/End and image dragging; baseline-specific download targets; no console warnings/errors. Local links, image metadata, Python syntax and public hygiene checked. Automated checks establish preservation, not a measured metal match.
- Refreshed generated galleries/indexes and root scope. Added 3D demo conventions to `AGENTS.md` and clarified that publishing does not require app-wide installation; `CLAUDE.md` still imports shared guidance.
- Existing library: nine generated gooey-section skills and six self-contained GSAP page-transition skills. Transition packages retain exact source curves, a 2.25s renderer, shared core, configurable modules, browser bundles, optional Astro adapter and demos. Prior parity, geometry, lifecycle and browser integration checks passed.
- Expanding scroll panel prototype and reusable prompt published on `main` on 2026-10-02 (`304818e`). Its background expands independently of content; the simplified layout and subtle backdrop fade passed desktop/mobile/reduced-motion browser checks.

## Current

- This public repository is `loouis/skills`; use the active checkout and verify its remote before changes. The library now contains 16 skills in 3 categories.
- The polished-metal skill is self-contained. Its public demo contains generic renders and code; generated `.blend` revisions and PNG masters are local build outputs. It preserves stainless identity even when the requested appearance is described as chrome-like.
- The expanding scroll panel remains a prototype under `prototypes/expanding-scroll-panel/`, excluded from installation and generated skill lists. Its README documents local preview and packaging work.
- Louis is testing the gooey skills in receiving projects. Their private generator remains the source of truth; see `AGENTS.md` before rebuilding.

## Decisions

- Create groups/categories with their first skill. Use `skills/<group>/<category>/<skill-name>/`; display `3d` as **3D**.
- Keep one skill per commit and publish only when requested. The new polished-metal skill's GitHub publication is authorised. No app-wide installation or website deployment is part of this change.
- Page transitions follow one skill per feel. “Suite” provisionally aliases Tidal sweep (`wave`); preserve source curves and mobile constants. The gooey Slosh notch matches the original lab and remains intentional.
- Blender presets are artistic starting points, not universal metal properties. Geometry changes remain separate from material-only work; reflection cards can influence indirect light.

## Next

- Package the expanding panel controller and invariant checks when requested.
- Use the new material workflow on other scenes and adjust from observed defects. Blender versions other than 5.2.1 and physical-device browser behavior remain unverified.
- Continue transition testing in receiving sites, including real navigation and physical devices; clarify the Suite alias only if a different shape is identified.

## Blockers

- None for the packaged skill. No private source-project dependency or external render asset is required.

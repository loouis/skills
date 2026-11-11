# Skills

Agent skills for web designers and 3D builders using [Claude Code](https://claude.com/claude-code), Codex and other AI coding agents.

**Browse every skill with its live demo at [loouis.github.io/skills](https://loouis.github.io/skills/).**

![Gooey section edges: nine liquid scroll effects between page sections](assets/skills-preview.jpg)

The section and page-transition skills rebuild effects from Louis's motion labs, with the original engine, a working demo and parity checks. Vector masking skills package geometry and masking methods with original studies. The 3D skills package material and lighting workflows, tested helpers and original Blender-rendered studies.

Start with the section edges:

1. **[Gooey section: Goo](skills/ui/sections/gooey-section-goo)**
   The default feel. The boundary between two sections acts like a liquid surface pulled by scroll speed.
2. **[Gooey section: Taffy](skills/ui/sections/gooey-section-taffy)**
   Stretches while you scroll, then drops, overshoots and wobbles once when you let go.
3. **[Gooey section: Wave](skills/ui/sections/gooey-section-wave)**
   A broad, flowing crest with a soft shoulder. The calm one.

Browse [the live site](https://loouis.github.io/skills/), [all demos and their prompts](DEMOS.md), or the [screenshot gallery](SCREENSHOTS.md).

For logos and illustrations, explore [Masking](skills/ui/masking/README.md), starting with [Vector Masking](skills/ui/masking/vector-masking): whole vector pieces, accurate silhouettes, clean joins and controlled gaps.

For page transitions, [Page Transitions](skills/ui/page-transitions/README.md) has six hand-drawn GSAP transitions that swell to cover a route change and reveal the next page, such as [Wide Tide](skills/ui/page-transitions/gsap-transition-wide-tide).

For motion, [Logo Mask Motion](skills/motion/logo/logo-mask-motion) animates a line-drawn logo piece by piece and lands on the exact artwork, and [Motion Director Film](skills/motion/film/motion-director-film) makes finished product films and showreels in code with Remotion or GSAP.

For rendering, explore [3D](skills/3d/README.md), starting with [Blender polished chrome](skills/3d/materials/blender-polished-chrome): mirror-polished metals, reflection control and preservation checks.

For interiors, [Coastal Interior Render](skills/3d/interiors/coastal-interior-render) builds photoreal Blender kitchens and living rooms in natural daylight, with annotated realism reviews.

For Blender water and fluid effects, [Blender Screen Water](skills/3d/fluids/blender-screen-water) packages a clear FLIP sheet, clustered bubbles, dark reflections and partial-loop playback, with portable job preparation and an original material study.

For clear studio water, [Water Optics · Clear Studio](skills/3d/fluids/water-optics-clear-studio) includes droplet, air-cavity and folded-surface benches, curved product contact, small local ripples, reflected-lettering diagnosis and scored reference review.

For suspended product splashes, [Water · Product Splash](skills/3d/fluids/water-product-splash) covers folded sheets, torn rims, droplets, reflection control and a workflow for adding tested lessons as the work develops.

For sunlit pools, [Water Pool · Sunlight](skills/3d/fluids/water-pool-sunlight) puts caustics (the net of sunlight) on the pool floor and underwater sun rays through the water, both read from one light map so every ray stands on a bright patch of floor.

---

## Agent support

Each skill is a plain folder: a `SKILL.md` playbook plus the files it needs.

- **Claude Code**: run `python3 install.py` to link every skill into `~/.claude/skills/`. Ask in your own words ("add the taffy goo between these sections") or call a skill directly with `/gooey-section-taffy`.
- **Codex**: copy a skill folder into your Codex skills directory. `agents/openai.yaml` gives Codex its display name, short description and default prompt. Invoke it with `$gooey-section-taffy`.
- **Cursor and other agents**: point the agent at the skill's `SKILL.md` and let it follow the steps and linked references.

---

## How these skills work

### Ship the engine, not a description
A feel lives in tuned numbers. A skill carries the original code as an asset, so the agent copies it instead of approximating it.

### Every feel has a demo
Each visual skill has a standalone `demo/index.html`, a rendered `preview.jpg` and the prompt that recreates it.

### Verified against the original
Skills built from a lab are checked frame by frame against that lab before they are published.

---

## Repo structure

```txt
skills/
  ui/
    README.md
    sections/           # gooey section edges
    page-transitions/   # hand-drawn GSAP page transitions
    masking/            # vector masking
  motion/
    README.md
    logo/               # logo mask motion
    film/               # short films made in code
  3d/
    README.md
    fluids/             # Blender water: screen water, clear studio, splash, pool sunlight
    interiors/          # coastal interior render
    materials/          # polished chrome
scripts/                # landing pages, previews, gallery, validation
install.py              # link skills into Claude Code
```

Folder contract:

```txt
skills/<group>/<category>/<skill-name>/
  SKILL.md            # required: frontmatter (name, description) + workflow
  README.md           # generated landing page: search title, preview, tags (edit scripts/skill-pages.json)
  REFERENCES.md       # optional: links only
  agents/openai.yaml  # interface metadata: display name, short description, default prompt
  assets/             # optional: code and files the skill hands to the agent
  references/         # optional: longer docs the skill points to
  scripts/            # optional: helper scripts
  demo/               # optional: visual proof
    index.html        # standalone HTML, CSS and JavaScript
    PROMPT.md         # minimal, recreation and remix prompts
    preview.jpg       # 1280 x 720 browser render
```

Conventions:
- `SKILL.md` is what the agent loads and follows. Keep it under about 500 lines and procedural: steps, defaults, guardrails.
- The `description` says what the skill does and when to use it. That is what an agent reads to decide.
- `REFERENCES.md` is links only.
- Each skill folder has a generated `README.md`, the page GitHub shows when you open the folder. Its title and tags come from `scripts/skill-pages.json`; run `node scripts/build-gallery.cjs` after changing a skill.
- Skill names are unique across categories, because Claude Code installs them side by side.

---

## Current library

<!-- library:start -->
This snapshot contains **24 skills** across 8 categories. `find skills -name SKILL.md | sort` is the source of truth.

### 3D Fluids (4)

[Category guide](skills/3d/fluids/README.md)

- [`blender-screen-water`](skills/3d/fluids/blender-screen-water) - Clear FLIP water sheets, clustered bubbles and loops
- [`water-optics-clear-studio`](skills/3d/fluids/water-optics-clear-studio) - Clear water, curved contact and controlled reflections
- [`water-pool-sunlight`](skills/3d/fluids/water-pool-sunlight) - Floor sunlight and sun rays for pool water, from one light map
- [`water-product-splash`](skills/3d/fluids/water-product-splash) - Folded water sheets, torn rims and product splashes

### 3D Interiors (1)

[Category guide](skills/3d/interiors/README.md)

- [`coastal-interior-render`](skills/3d/interiors/coastal-interior-render) - Warm coastal interiors with rigorous realism review

### 3D Materials (1)

[Category guide](skills/3d/materials/README.md)

- [`blender-polished-chrome`](skills/3d/materials/blender-polished-chrome) - Mirror-polished metal materials and studio reflections

### Film Skills (1)

[Category guide](skills/motion/film/README.md)

- [`motion-director-film`](skills/motion/film/motion-director-film) - Direct, animate, score and QA a finished short film in code

### Logo Skills (1)

[Category guide](skills/motion/logo/README.md)

- [`logo-mask-motion`](skills/motion/logo/logo-mask-motion) - Move the pieces of a line-drawn mark with masks and land on the artwork

### Masking Skills (1)

[Category guide](skills/ui/masking/README.md)

- [`vector-masking`](skills/ui/masking/vector-masking) - Accurate vector masks, clean joins and controlled gaps

### Page Transition Skills (6)

[Category guide](skills/ui/page-transitions/README.md)

- [`gsap-transition-diagonal-tide`](skills/ui/page-transitions/gsap-transition-diagonal-tide) - Diagonal Tide draw, swell and reveal transition
- [`gsap-transition-double-swell`](skills/ui/page-transitions/gsap-transition-double-swell) - Double Swell draw, swell and reveal transition
- [`gsap-transition-figure-eight`](skills/ui/page-transitions/gsap-transition-figure-eight) - Figure Eight draw, swell and reveal transition
- [`gsap-transition-signature-loop`](skills/ui/page-transitions/gsap-transition-signature-loop) - Signature Loop draw, swell and reveal transition
- [`gsap-transition-suite`](skills/ui/page-transitions/gsap-transition-suite) - Suite draw, swell and reveal transition
- [`gsap-transition-wide-tide`](skills/ui/page-transitions/gsap-transition-wide-tide) - Wide Tide draw, swell and reveal transition

### Section Skills (9)

[Category guide](skills/ui/sections/README.md)

- [`gooey-section-drift`](skills/ui/sections/gooey-section-drift) - Crest that surfs sideways as you scroll
- [`gooey-section-elastic`](skills/ui/sections/gooey-section-elastic) - Springy edge that overshoots and twangs back
- [`gooey-section-goo`](skills/ui/sections/gooey-section-goo) - Tight sticky bulge with sinking flanks
- [`gooey-section-honey`](skills/ui/sections/gooey-section-honey) - Heavy blob: slow rise, very slow droop
- [`gooey-section-peel`](skills/ui/sections/gooey-section-peel) - Fast drain from full stretch, slow peeling tail
- [`gooey-section-slosh`](skills/ui/sections/gooey-section-slosh) - Liquid lean: rises one side, dips the other
- [`gooey-section-taffy`](skills/ui/sections/gooey-section-taffy) - Stretches on scroll, snaps back with one wobble
- [`gooey-section-twin`](skills/ui/sections/gooey-section-twin) - Main bulge plus a smaller blob beside it
- [`gooey-section-wave`](skills/ui/sections/gooey-section-wave) - Broad flowing crest pulled by scroll speed
<!-- library:end -->

---

## Install

```bash
git clone https://github.com/loouis/skills.git
cd skills
python3 install.py
```

This links every skill into `~/.claude/skills/`. Because they are links, `git pull` updates them in place. Rerun `install.py` after adding a skill; it only replaces links that are broken or already point into this repo.

To install a single skill instead:

```bash
ln -s "$PWD/skills/ui/sections/gooey-section-taffy" ~/.claude/skills/
```

---

## Adding a skill

1. Pick a group and category under `skills/`, such as `skills/ui/sections/`, or create one with a `README.md` (copy `skills/ui/sections/README.md`).
2. Create `skills/<group>/<category>/<skill-name>/SKILL.md`, then add `agents/openai.yaml` and, if it has sources, `REFERENCES.md`.
3. For a visual skill, add `demo/index.html` and `demo/PROMPT.md`, then render the preview:
   ```bash
   node scripts/build-previews.cjs <skill-name>
   ```
   A demo can define `window.__demoPose()` to set up the frame worth capturing.
4. Refresh the lists and check the contract:
   ```bash
   node scripts/build-gallery.cjs
   node scripts/validate-skills.cjs
   ```
5. Commit: small commits, one skill each, `Add <skill-name> skill` or `Update <skill-name> skill`. Run `python3 install.py` only when local Claude Code installation is wanted; publishing does not require it.

---

## License

MIT. Use, adapt and ship these skills in your own work; keep the copyright notice. See [LICENSE](LICENSE).

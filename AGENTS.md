# skills — repo guide

Louis's agent skills, published at https://github.com/loouis/skills. **This repo is public.** Multiple local checkouts may exist; use the active project checkout and verify its `origin` before making changes. Resolve the private labs generator location before rebuilding generated skills in a different checkout. Skills live in category folders, each skill with `SKILL.md`, `REFERENCES.md`, `agents/openai.yaml` and, for visual skills, a `demo/`.

## What to do here
- Add new skills under `skills/<group>/<category>/`, for example `skills/ui/sections/`.
- Improve existing skills: `SKILL.md` first, then `REFERENCES.md`, then the demo.
- Keep skills procedural: steps, defaults, guardrails, checks.

## Working conventions
- Commit messages here carry no AI co-author trailer (no `Co-Authored-By: Claude…` line), and the repo never names other people's repos as the inspiration for its layout. Louis's instruction; it overrides any default attribution.
- Read `STATUS.md` before starting and update it after substantive work.
- Commit after every completed change, one skill per commit (`Add <skill-name> skill` / `Update <skill-name> skill`). Pushing publishes to the public repo, so push when Louis asks for it or confirms.
- Commits here use GitHub's no-reply address for `loouis`, set automatically by `~/.gitconfig` for any `github.com/loouis/...` remote, so Louis's email stays out of the public history. Don't add a per-repo `user.email`.

## Folder contract
See README.md → "Repo structure". In short: `skills/<group>/<category>/<skill-name>/` with `SKILL.md` (frontmatter `name` = folder name, a `description` that says what and when), `agents/openai.yaml` (`display_name`, `short_description`, `default_prompt` invoking `$<skill-name>`), `REFERENCES.md` (links only), and optional `assets/`, `references/`, `scripts/`, `demo/` (`index.html`, `PROMPT.md`, `preview.jpg` at 1280×720). Every group and category has a `README.md`; the category skills tables, the group category lists and the root README's library list are generated between `<!-- skills:… -->`, `<!-- categories:… -->` and `<!-- library:… -->` markers.

## Commands
- `python3 install.py` — link every skill into `~/.claude/skills/` (`--dry-run` to preview).
- `node scripts/build-previews.cjs [skill-name…]` — render `demo/preview.jpg` and `assets/skills-preview.jpg` (needs puppeteer; `NODE_PATH` may point at an existing install).
- `node scripts/build-gallery.cjs` — regenerate DEMOS.md, SCREENSHOTS.md/.html and the generated README lists.
- `node scripts/validate-skills.cjs` — check every skill against the contract. Run before committing.

## Public hygiene (check before every commit)
- No client or project names, no private file paths, no emails, keys or tokens, nothing from private repos beyond what a skill needs. The validator flags private paths.

## gooey-section family
- Generated: the sources (engine, `engine.md`, `demo.html`, `PROMPT.md`, `REFERENCES.md`, per-variant text and `build.py`) live in Louis's private labs repo at `../labs/skills/gooey-section/`, next to the original lab. Edit them there and run `python3 skills/gooey-section/build.py` from the labs repo; it writes into `skills/ui/sections/` here. Never hand-edit `skills/ui/sections/gooey-section-*`.
- The engine must stay a 1:1 port of the original lab. After changing it or rebuilding, run `node tests/gooey-section-parity.cjs` and `node tests/gooey-section-browser.cjs` in the labs repo.

## hand-drawn page transitions
- Six self-contained `gsap-transition-*` skills live under `skills/ui/page-transitions/`. Keep shared `assets/core/` files identical across the family except `config.mjs`, which selects each package's default. These packages are maintained here; they do not depend on the private gooey generator.
- Preserve the exact source curves and 2.25s renderer. “Suite” provisionally aliases Tidal sweep (`wave`); see each package's `references/motion.md` for the six IDs, mobile constants and customization rules.
- After core changes, run `node scripts/build-bundle.mjs` inside each affected skill, then `node --test scripts/*.test.mjs` and `node scripts/build-bundle.mjs --check`. The root validator checks shared-core consistency and public paths across module/TypeScript/Python assets too.
- Demos use a pinned GSAP CDN or the skill's loopback `scripts/serve_preview.py --gsap <local-gsap.min.js>` for offline playback. Keep each demo's selected default and preview aligned with its skill.

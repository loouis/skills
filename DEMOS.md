# Skill Demos

Every visual skill has a portable demo, a rendered preview and the exact prompt to recreate or remix it.

## Folder contract

```text
skills/<category>/<skill-name>/
  demo/
    index.html     # standalone page: inline CSS, relative paths, no build step
    PROMPT.md      # minimal, recreation and remix prompts
    preview.jpg    # 1280 x 720 browser render
```

A demo may load the skill's own files from `../assets/`, so the skill folder stays the unit you copy.

## Run a demo

Open `demo/index.html` straight in a browser, or serve the skill folder:

```bash
python3 -m http.server 4173 -d skills/<category>/<skill-name>
```

Then visit http://localhost:4173/demo/.

## Rebuild

```bash
node scripts/build-previews.cjs      # render demo/preview.jpg (needs puppeteer)
node scripts/build-gallery.cjs       # this file, SCREENSHOTS.md/.html, README lists
node scripts/validate-skills.cjs     # check every skill against the folder contract
```

## Library coverage

- Total: 15
- With demos: 15
- ui/page-transitions: 6
- ui/sections: 9

## Demo index

| Skill | Category | Demo | Preview | Prompt |
| --- | --- | --- | --- | --- |
| gsap-transition-diagonal-tide | ui/page-transitions | [Open](skills/ui/page-transitions/gsap-transition-diagonal-tide/demo/index.html) | [Preview](skills/ui/page-transitions/gsap-transition-diagonal-tide/demo/preview.jpg) | [Prompt](skills/ui/page-transitions/gsap-transition-diagonal-tide/demo/PROMPT.md) |
| gsap-transition-double-swell | ui/page-transitions | [Open](skills/ui/page-transitions/gsap-transition-double-swell/demo/index.html) | [Preview](skills/ui/page-transitions/gsap-transition-double-swell/demo/preview.jpg) | [Prompt](skills/ui/page-transitions/gsap-transition-double-swell/demo/PROMPT.md) |
| gsap-transition-figure-eight | ui/page-transitions | [Open](skills/ui/page-transitions/gsap-transition-figure-eight/demo/index.html) | [Preview](skills/ui/page-transitions/gsap-transition-figure-eight/demo/preview.jpg) | [Prompt](skills/ui/page-transitions/gsap-transition-figure-eight/demo/PROMPT.md) |
| gsap-transition-signature-loop | ui/page-transitions | [Open](skills/ui/page-transitions/gsap-transition-signature-loop/demo/index.html) | [Preview](skills/ui/page-transitions/gsap-transition-signature-loop/demo/preview.jpg) | [Prompt](skills/ui/page-transitions/gsap-transition-signature-loop/demo/PROMPT.md) |
| gsap-transition-suite | ui/page-transitions | [Open](skills/ui/page-transitions/gsap-transition-suite/demo/index.html) | [Preview](skills/ui/page-transitions/gsap-transition-suite/demo/preview.jpg) | [Prompt](skills/ui/page-transitions/gsap-transition-suite/demo/PROMPT.md) |
| gsap-transition-wide-tide | ui/page-transitions | [Open](skills/ui/page-transitions/gsap-transition-wide-tide/demo/index.html) | [Preview](skills/ui/page-transitions/gsap-transition-wide-tide/demo/preview.jpg) | [Prompt](skills/ui/page-transitions/gsap-transition-wide-tide/demo/PROMPT.md) |
| gooey-section-drift | ui/sections | [Open](skills/ui/sections/gooey-section-drift/demo/index.html) | [Preview](skills/ui/sections/gooey-section-drift/demo/preview.jpg) | [Prompt](skills/ui/sections/gooey-section-drift/demo/PROMPT.md) |
| gooey-section-elastic | ui/sections | [Open](skills/ui/sections/gooey-section-elastic/demo/index.html) | [Preview](skills/ui/sections/gooey-section-elastic/demo/preview.jpg) | [Prompt](skills/ui/sections/gooey-section-elastic/demo/PROMPT.md) |
| gooey-section-goo | ui/sections | [Open](skills/ui/sections/gooey-section-goo/demo/index.html) | [Preview](skills/ui/sections/gooey-section-goo/demo/preview.jpg) | [Prompt](skills/ui/sections/gooey-section-goo/demo/PROMPT.md) |
| gooey-section-honey | ui/sections | [Open](skills/ui/sections/gooey-section-honey/demo/index.html) | [Preview](skills/ui/sections/gooey-section-honey/demo/preview.jpg) | [Prompt](skills/ui/sections/gooey-section-honey/demo/PROMPT.md) |
| gooey-section-peel | ui/sections | [Open](skills/ui/sections/gooey-section-peel/demo/index.html) | [Preview](skills/ui/sections/gooey-section-peel/demo/preview.jpg) | [Prompt](skills/ui/sections/gooey-section-peel/demo/PROMPT.md) |
| gooey-section-slosh | ui/sections | [Open](skills/ui/sections/gooey-section-slosh/demo/index.html) | [Preview](skills/ui/sections/gooey-section-slosh/demo/preview.jpg) | [Prompt](skills/ui/sections/gooey-section-slosh/demo/PROMPT.md) |
| gooey-section-taffy | ui/sections | [Open](skills/ui/sections/gooey-section-taffy/demo/index.html) | [Preview](skills/ui/sections/gooey-section-taffy/demo/preview.jpg) | [Prompt](skills/ui/sections/gooey-section-taffy/demo/PROMPT.md) |
| gooey-section-twin | ui/sections | [Open](skills/ui/sections/gooey-section-twin/demo/index.html) | [Preview](skills/ui/sections/gooey-section-twin/demo/preview.jpg) | [Prompt](skills/ui/sections/gooey-section-twin/demo/PROMPT.md) |
| gooey-section-wave | ui/sections | [Open](skills/ui/sections/gooey-section-wave/demo/index.html) | [Preview](skills/ui/sections/gooey-section-wave/demo/preview.jpg) | [Prompt](skills/ui/sections/gooey-section-wave/demo/PROMPT.md) |

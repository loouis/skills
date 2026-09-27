---
name: gsap-transition-double-swell
description: Build the Double Swell hand-drawn GSAP page transition. Two rounded waves rise and fall across the screen. Use when the user asks for Double Swell, the double-swell transition, or this named draw-swell-cover-reveal effect on a website. Ships reusable curves, adaptive portrait fronts, a covered routing lifecycle and a working demo.
---

# Double Swell page transition

Two rounded waves rise and fall across the screen. One continuous stroke travels across the screen, swells to cover the route change, then carries its tail forward to reveal the next page.

## Use the bundled engine

1. Read the host's router and animation lifecycle before wiring navigation. Choose stable shape ID **`double-swell`**. This package defaults to it; all six names remain available through `getShape()`.
2. Copy `assets/core/` into the project and import `transition.css`. Reuse GSAP core. For plain script sites, use the equivalent `assets/hand-drawn.js` bundle. Do not substitute an approximate curve or require Barba/DrawSVG.
3. Mount one empty `.hand-drawn-transition` overlay outside the swapped route tree. Create the controller after mounting:

   ```js
   import { gsap } from 'gsap';
   import { createTransition } from './motion/transition.mjs';
   import './motion/transition.css';

   const transition = createTransition({
     overlay: document.querySelector('#page-ink'),
     gsap,
     variant: 'double-swell',
     color: '#202020', // replace with the site's opaque brand color
   });
   ```

4. Follow [integration.md](references/integration.md) for the `load → covered swap → ready reveal` contract, cleanup, scroll/focus responsibilities and framework wiring. Read the Astro section only for an Astro ClientRouter project; its ready-to-copy adapter is under `assets/adapters/astro/`.
5. Keep colors and layout specific to the receiving site. The demo uses generic text, system fonts and flat colors; no source-brand assets are required.

## Preserve the feel

| Phase | Reference behavior |
| --- | --- |
| 0–1s | Draw to 85% of the path. |
| 0.25–1s | Expand from stroke 65 to 880 in desktop coordinates. |
| 1s | Swap only under full cover; extend the hidden end to 100%. |
| 1–2.25s | Carry the tail forward and thin back to the starting width. |

The pure `frame()` renderer already applies quadratic `power1.inOut`. Drive time with GSAP `ease: 'none'`. Additional loading time belongs only at full cover. The study's 0.9s autoplay pauses are not part of this transition. Returning to a previous page uses the same forward gesture, not a reversed clock.

For portrait screens, map the centreline to the actual viewport before stroking, then scale the SVG uniformly. The reference portrait stroke is 110 → 1950 at 390 × 844. Its portrait cover is a newly validated extension of the reference treatment. The original normalized tail takes over at 1s under full coverage. Read [motion.md](references/motion.md) before changing geometry, cover widths, the responsive cutoff or front rounding. Do not stretch a square SVG to draw the portrait leading end.

Maintain one connected gesture: no unrelated cover fill, visible shape/origin switch, flash at handoff or reversed tail. Use an opaque solid ink color. Keep reduced-motion, cancellation, readiness and teardown behavior from the controller. Preserve native link eligibility and existing seamless handoffs in the host router.

Hide the scrollbar for the entire active transition while preserving its space with `scrollbar-gutter: stable` in the shared site styles. Use `overflow: hidden` for the scroll lock and restore the previous state on completion or interruption, so the page never jumps sideways. Follow the [scroll and input guidance](references/integration.md#scroll-and-input) when connecting the host scroll runtime.

## Accessibility

Honor the phone/browser's `prefers-reduced-motion` setting and any site motion-off preference. Skip the moving stroke and use static loading text or a still indicator; keep navigation, readiness and error handling functional without animation or artificial delay. The core handles the motion bypass; the host supplies accessible loading feedback. Keep polite status announcements outside the decorative overlay, preserve keyboard focus and clear loading/busy state on every exit. Follow the [reduced-motion and accessibility guidance](references/integration.md#accessibility-and-reduced-motion), including changes to the preference mid-transition and screen-reader checks.

## Check the result

- Run `node --test scripts/*.test.mjs` from this skill directory (Node 20+).
- Open `demo/index.html`, or run `python3 scripts/serve_preview.py`; the demo supports each shape, frame inspection, slow loading, cancellation, reduced motion and portrait ratios. Its pinned GSAP CDN needs network; `--gsap <local-gsap.min.js>` enables offline playback. Frame inspection is available without GSAP.
- Inspect frames 35/50 for the front, 59–61 for an opaque handoff, and 135 for complete cleanup. Check short/tall/rotated screens and run the receiving site's build/type checks.
- Verify slow/failing loads, repeat navigation, back/forward, reduced motion, focus/scroll restoration and component cleanup in the real router. Geometry tests alone do not establish browser lifecycle correctness.
- If core code changes, regenerate `assets/hand-drawn.js` with `node scripts/build-bundle.mjs`. Keep the other family packages' shared engine copies in sync; each package must remain self-contained.

See [provenance.md](references/provenance.md) for source parity and the distinction between approved mobile constants and new portrait extensions; [REFERENCES.md](REFERENCES.md) contains platform links.

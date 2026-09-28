# Expanding scroll panel prototype

A scroll study: an inset white panel rises over a sticky preceding section, expands to the viewport edges and loses its top corner radius. Its content keeps the same horizontal position, width, font sizes and card dimensions throughout the transition. Content moves vertically with normal page scrolling; it is not pinned to the screen.

Prototype first; the reusable skill is the next step after motion review. This folder is deliberately outside the installed skill library and generated galleries.

## Run

From the repository root:

```sh
python3 -m http.server 4173 --bind 127.0.0.1 --directory prototypes/expanding-scroll-panel
```

Open <http://127.0.0.1:4173>. No installation, build step, external fonts or animation dependencies are needed. Serve over HTTP so the browser can load the ES modules.

Use **Replay** and **Full width** to revisit the endpoints. **Tune** adjusts side margin, radius and completion position. Alignment guides show the stationary content boundaries. Reduced-motion preview removes both expansion and sticky overlap; the system preference always takes priority.

## Implementation

- `index.html`: preceding section, empty panel surface, sibling content and demo controls.
- `style.css`: responsive layout, sticky overlap, background clipping and static fallback.
- `expanding-panel.js`: reusable mount/update/destroy controller, named defaults and scroll storyboard.
- `demo.js`: optional prototype controls.

The wrapper occupies the available page width at every scroll position. Only the empty background's `clip-path` changes. The content is a sibling of that background, with its own stable width. Never animate the content ancestor's scale, width, horizontal padding or margin to create this effect.

The preceding section sticks inside the shared stage. A negative top margin brings the incoming panel into view at 78% of the viewport. Its higher stacking order covers the earlier section. No scroll locking or smoothing library is used.

Progress is `clamp((0.78 × viewportHeight − panelTop) / (0.72 × viewportHeight), 0, 1)`. A smoothstep maps that progress to side inset `24 → 0px` and top radius `20 → 0px`; the panel is fully expanded at 6% from the viewport top. These values live in `DEFAULTS`. Side inset is capped at the content gutter minus 8px on narrow viewports. The initial overlap is controlled independently by `-22svh` in CSS.

Scroll events schedule one animation frame; there is no permanent animation loop or delayed scrub. Resize, content size changes, font readiness and page restoration refresh the geometry. Call `destroy()` when unmounting in a client router. Without JavaScript or with reduced motion, the sections use normal flow and the panel stays full width.

## Review checklist

- Scroll down and up slowly: only the background edges and radius change.
- Compare the heading and cards at start, middle and end: horizontal bounds and line wrapping stay identical.
- At completion, side inset and radius are exactly zero.
- The old section stays behind the new one; there is no gap, horizontal overflow or blocked scrolling.
- Resize while partway through, including narrow phones and short landscape windows.
- Try the tuning controls, alignment guides, reset and reduced-motion preview.

## Validation

Browser checks cover desktop 1280×720 and mobile 390×844, with an additional 320×640 control-fit check. Desktop measurements at the start, midpoint, end and reverse have identical content, heading and card horizontal bounds and dimensions; mobile start/end checks agree. No horizontal overflow was observed. The full-width endpoint has 0px inset and 0px radius. Reduced-motion preview removes clipping, sticky positioning and negative overlap. Physical-device Safari and OS-level preference switching remain untested.

Visual reference: [Scale homepage](https://scale.com/). This prototype uses original demo text and CSS artwork.

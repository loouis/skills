# Expanding scroll panel prototype

A scroll study: an inset white panel rises over a sticky preceding section, expands to the viewport edges and loses its top corner radius. Its content keeps the same horizontal position, width, font sizes and card dimensions throughout the transition. Content moves vertically with normal page scrolling; it is not pinned to the screen.

The motion has been reviewed. The prototype now contains only the large section headings and cards, without branding, eyebrows, arrows, supporting copy or demo controls. The reusable skill is the next step. This folder is deliberately outside the installed skill library and generated galleries.

## Run

From the repository root:

```sh
python3 -m http.server 4173 --bind 127.0.0.1 --directory prototypes/expanding-scroll-panel
```

Open <http://127.0.0.1:4173>. No installation, build step, external fonts or animation dependencies are needed. Serve over HTTP so the browser can load the ES modules.

Scroll down and back up to view the transition. Adjust side margin, radius and completion position in `DEFAULTS` in `expanding-panel.js`. System reduced-motion preferences remove both expansion and sticky overlap.

## Implementation

- `index.html`: preceding section, empty panel surface and sibling content.
- `style.css`: responsive layout, sticky overlap, background clipping and static fallback.
- `expanding-panel.js`: reusable mount/update/destroy controller, named defaults and scroll storyboard.
- `demo.js`: mounts the scroll animation.

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
- Confirm the page shows only the section headings and cards.

## Validation

The original controller passed desktop 1280×720 start/midpoint/end/reverse and mobile 390×844 start/end geometry checks. Full expansion reaches 0px inset and radius, with no horizontal overflow. Reduced-motion behavior was checked using the original preview controls before their removal. The presentation cleanup leaves that controller unchanged. Physical-device Safari and OS-level preference switching remain untested.

Visual reference: [Scale homepage](https://scale.com/). This prototype uses original demo text and CSS artwork.

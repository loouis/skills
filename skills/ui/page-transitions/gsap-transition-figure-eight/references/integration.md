# Integration

## Core, independent of the router

Copy `assets/core/` into the project's motion directory. Import `transition.css`, reuse the site's GSAP core dependency, and mount an empty `.hand-drawn-transition` overlay under `body`, outside the route subtree and any transformed ancestor. Keep one live controller per overlay. Imports are safe before DOM mount; call `createTransition()` only on the client after mounting.

```js
import { gsap } from 'gsap';
import { createTransition, visibleMediaReady } from './motion/transition.mjs';
import './motion/transition.css';

const transition = createTransition({
  overlay: document.querySelector('#page-ink'),
  gsap,
  variant: 'wide-tide', // replace with the requested skill's stable ID
  color: '#202020',     // replace with an opaque brand token
});

// Call from the existing router's preparation/commit hooks.
await transition.run({
  load: signal => router.prepare(url, { signal }),
  swap: (destination, signal) => router.commit(destination, { signal }),
  ready: () => visibleMediaReady(),
});

// On component unmount or integration replacement:
transition.destroy();
```

`router.prepare`/`router.commit` above describe the host router's responsibilities; they are not library APIs. Fetch while covering, then commit only after `covered` resolves. For routers with lifecycle events, use `begin(signal)`, await `session.covered` in the loader, then `session.reveal(readinessPromise)` after the actual swap. The Astro example demonstrates this split. Put focus transfer and scroll restoration in the host's commit lifecycle.

`run()` returns false when superseded/aborted; it rethrows load/commit failures so the router can show its normal error view. A superseded session aborts its signal, stops its tween and settles pending animation/readiness promises. A load that ignores cancellation is prevented from committing. A custom asynchronous commit must also respect its signal; the motion controller cannot undo an already-committed page.

Readiness waits for visible eager images and fonts, capped at five seconds by default. Broken media settles safely. If the above-fold experience depends on video or hydration, include that readiness promise explicitly. A readiness timeout allows reveal; it does not cancel the router's network load. Keep the router's existing fetch timeout/error handling.

## Non-bundled HTML

Load the host's GSAP core script, `assets/hand-drawn.js`, and `assets/core/transition.css`. The generated bundle exposes `window.HandDrawn.createTransition()` with the same API. The demo uses a pinned GSAP CDN script; applications can use their own installed build. No DrawSVG plugin, React or Barba is required. `scripts/build-bundle.mjs` rebuilds the classic bundle after core edits.

## Astro ClientRouter

Copy the files exactly as follows, then adjust imports if the project uses a different layout:

| Bundled source | Destination |
| --- | --- |
| `assets/core/*` | `src/motion/hand-drawn/*` |
| `assets/adapters/astro/PageTransition.astro` | `src/components/PageTransition.astro` |
| `assets/adapters/astro/page-transition.ts` | `src/scripts/page-transition.ts` |

Mount `<PageTransition variant="wide-tide" color="#202020" />` once in the shared layout, using the selected skill ID. Keep the existing `<ClientRouter />`. The overlay persists between shared-layout pages; `astro:before-preparation` wraps the loader with the cover promise. `astro:before-swap` skips the native snapshot animation while retaining the document swap. `astro:page-load` waits for visible resources then reveals.

The adapter lets Astro own anchor eligibility, external URLs, modified clicks, downloads, forms and history. It bypasses same-page/hash navigation and `info.transition === 'seamless'` for sites with another approved handoff. Pages outside the shared layout cancel the effect. Reduced motion uses the same router flow without animation; changes during a transition settle the clock and clear the overlay. HMR disposes listeners and the controller.

The persisted overlay retains its configuration. For a site-wide theme/variant change, destroy and recreate the controller deliberately instead of mounting duplicate overlays. Preserve any existing scroll-to-next effect, focus management and native link behavior.

## Accessibility and reduced motion

Respect `prefers-reduced-motion: reduce` before starting a transition, including the preference exposed by a phone's accessibility settings. The core already checks this preference and responds to changes while running. If the site also offers a motion-off setting, make the host bypass the effect when either preference requests less motion. A site preference must not silently re-enable motion disabled by the operating system.

Use a non-animated loading alternative. Keep the current page visible while the destination loads, show a static “Loading…” label or still icon with text when feedback is needed, and swap directly when the router can commit. Do not substitute a spinner, shimmer, pulse, zoom, slide or fade for someone requesting no motion. Do not add the normal 2.25s duration as an artificial delay. Keep the actual fetch, readiness, timeout, cancellation and error paths working even when no animation plays; never depend on an animation-end event to complete navigation.

The bundled controller provides the motion bypass; the receiving site's router must supply the static loading feedback and accessibility state described here. The decorative SVG overlay remains `aria-hidden="true"`. Put the loading message outside that overlay and outside any hidden or inert subtree. Reuse one persistent `role="status"` region with polite announcements rather than moving focus into the message. Update it when loading starts and settles, without announcing frames or repeated progress ticks. If the router already announces the new page, avoid a duplicate completion announcement. Mark the updating content region `aria-busy="true"` while appropriate, and clear it on success, failure or cancellation; keep the status region outside the busy region so its message is not deferred with the content update.

Keep the status text readable against its background and do not communicate loading or errors through color alone. Preserve the router's keyboard focus, document-title and history behavior. After a route swap, ensure focus reaches the destination's meaningful content through the host's existing focus strategy; preserve hash targets and history restoration. A static status message must not steal focus or create a keyboard trap. Keep ordinary links and failure/retry navigation usable.

Skip the decorative overlay and animation-only scroll lock in this mode. If reduced motion is enabled mid-transition, stop the moving effect, clear its overlay/lock and continue the pending navigation with static feedback. Remove stale status/busy state on completion, failure, abort, superseding navigation and teardown. Use the active navigation's identity so an older request cannot clear the newer request's loading state.

Verify the system/browser preference before loading the page and when changed during cover or reveal. Check slow and failed loads, repeated navigation, back/forward and keyboard-only use in both modes. Check announcements with a screen reader and the real phone accessibility preference in the receiving site. An animated-demo checkbox or a geometry test alone does not establish accessibility compliance.

## Scroll and input

Hide the scrollbar while the transition is active, from the start of cover through the loading hold and the end of reveal. Reserve its space before the animation starts so hiding and restoring it cannot change the page width or make the content jump sideways. Keep the gutter rule in the shared site styles on both routes:

```css
html { scrollbar-gutter: stable; }
html[data-page-transition-active] { overflow: hidden; }
```

Manage the active marker through the host's `lock()` callback, alongside its existing scroll runtime. Keep the lock active across the route swap; reapply the marker if the router replaces the root attributes. The returned cleanup callback must restore the previous scroll/overflow state on completion, cancellation, failure or destroy. Skip the lock when reduced motion bypasses the animation.

Use `overflow: hidden` for the active lock: `overflow: clip` can discard the reserved gutter and cause the sideways jump. Override an existing smooth-scroll stopped-state rule if it uses `clip`. The overlay blocks pointer input, but does not hide the scrollbar or lock scrolling by itself. Keep this integration in the host rather than creating another scroll runtime.

Check a page with a visible scrollbar and navigate to both long and short pages. The content's horizontal position should stay fixed when the lock starts, through the covered swap, and when scrolling is restored.

## Verification in the receiving project

Run the bundled geometry/lifecycle tests, then the host's build/type checks. In the browser check normal navigation, back/forward, repeated navigation, loading failure/slow readiness, reduced motion, hash/external/modified links, and cleanup. Inspect both sides of the 1s handoff and the end at 2.25s. Confirm no exposed corner or cap, no overlay left blocking interaction, and no position jump caused by scroll locking.

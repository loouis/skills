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

## Scroll and input

The overlay blocks pointer input while active. If the host requires scroll/keyboard locking, pass `lock()` returning a cleanup callback. Coordinate that lock with the existing scroll runtime; restore its previous state on idle, cancellation and destroy. Keep `scrollbar-gutter: stable` where supported. If an existing smooth-scroll stop mode uses `overflow: clip`, consider the site's tested `overflow: hidden` override so the gutter does not disappear. Do not create another scroll runtime or impose global overflow rules inside this skill.

## Verification in the receiving project

Run the bundled geometry/lifecycle tests, then the host's build/type checks. In the browser check normal navigation, back/forward, repeated navigation, loading failure/slow readiness, reduced motion, hash/external/modified links, and cleanup. Inspect both sides of the 1s handoff and the end at 2.25s. Confirm no exposed corner or cap, no overlay left blocking interaction, and no position jump caused by scroll locking.

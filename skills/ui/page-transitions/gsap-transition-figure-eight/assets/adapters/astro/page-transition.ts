// Copy to src/scripts/page-transition.ts. Keep the existing Astro ClientRouter.
import { gsap } from 'gsap';
import type { TransitionBeforePreparationEvent, TransitionBeforeSwapEvent } from 'astro:transitions/client';
import { createTransition, visibleMediaReady } from '../motion/hand-drawn/transition.mjs';

const overlay = document.getElementById('hand-drawn-transition');
if (overlay) {
  const transition = createTransition({
    overlay, gsap,
    variant: overlay.dataset.variant,
    color: overlay.dataset.color ?? '#202020',
    // Supply a host scroll lock here if needed. Preserve its existing gutter and
    // release it on idle. Do not create a second smooth-scroll instance.
  });
  let active: { event: TransitionBeforePreparationEvent; session: ReturnType<typeof transition.begin>; swapped: boolean } | undefined;
  const prepare = (event: TransitionBeforePreparationEvent) => {
    transition.cancel(); active = undefined;
    const samePage = event.from.pathname === event.to.pathname && event.from.search === event.to.search;
    if (samePage || event.info?.transition === 'seamless' || event.defaultPrevented) return;
    const session = transition.begin(event.signal);
    const entry = { event, session, swapped: false };
    active = entry;
    const loader = event.loader;
    event.loader = async () => {
      try { await Promise.all([loader(), session.covered]); }
      catch (error) { session.cancel(); throw error; }
      if (event.defaultPrevented || event.signal.aborted) session.cancel();
      // A destination outside the shared layout should use the router's normal
      // transition, since its overlay will not persist through the swap.
      if (!event.newDocument.getElementById('hand-drawn-transition')) session.cancel();
    };
  };
  const beforeSwap = (event: TransitionBeforeSwapEvent) => {
    if (active?.event.signal !== event.signal || !active.session.current()) return;
    // Keep the real DOM swap while skipping native snapshot animation.
    void event.viewTransition.ready.catch(() => {});
    event.viewTransition.skipTransition();
    active.swapped = true;
  };
  const pageLoad = async () => {
    const entry = active;
    if (!entry?.swapped || !entry.session.current()) return;
    await entry.session.reveal(visibleMediaReady(), 5000);
    if (active === entry) active = undefined;
  };
  document.addEventListener('astro:before-preparation', prepare);
  document.addEventListener('astro:before-swap', beforeSwap);
  document.addEventListener('astro:page-load', pageLoad);
  if (import.meta.hot) import.meta.hot.dispose(() => {
    transition.destroy(); active = undefined;
    document.removeEventListener('astro:before-preparation', prepare);
    document.removeEventListener('astro:before-swap', beforeSwap);
    document.removeEventListener('astro:page-load', pageLoad);
  });
}

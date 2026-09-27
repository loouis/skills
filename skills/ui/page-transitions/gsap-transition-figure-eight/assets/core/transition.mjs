import { getShape } from './shapes.mjs';
import { createPainter } from './painter.mjs';
import { createDriver } from './driver.mjs';
import { DEFAULT_VARIANT } from './config.mjs';

export { getShape, SHAPES, VARIANTS } from './shapes.mjs';
export { TIMING, frame, portraitShape } from './geometry.mjs';

export function visibleMediaReady(doc = document) {
  const height = doc.defaultView?.innerHeight ?? 0;
  const images = [...doc.images].filter(image => {
    const bounds = image.getBoundingClientRect();
    return image.loading !== 'lazy' && bounds.bottom > 0 && bounds.top < height;
  });
  return Promise.all([doc.fonts?.ready, ...images.map(image => image.decode().catch(() => {}))]);
}

// Overlay must live outside the route subtree, under body, with the shared CSS.
// lock() is an optional host-owned scroll/input lock; it returns an unlock callback.
export function createTransition({
  overlay, gsap, variant = DEFAULT_VARIANT, shape = getShape(variant), color = '#202020',
  portraitMaxWidth = 1024, portrait = {}, lock = () => () => {},
}) {
  const painter = createPainter(overlay, { shape, color, portraitMaxWidth, portrait });
  const view = overlay.ownerDocument.defaultView;
  const reduced = view.matchMedia('(prefers-reduced-motion: reduce)');
  let unlock;
  overlay.dataset.phase = 'idle';
  const driver = createDriver({
    gsap, paint: painter.paint, reducedMotion: () => reduced.matches,
    onPhase(phase) {
      overlay.dataset.phase = phase;
      if (phase === 'idle') { const release = unlock; unlock = undefined; release?.(); }
      else if (!unlock) unlock = lock();
    },
  });
  const motionChanged = () => { if (reduced.matches) driver.reduce(); };
  const pageHidden = () => driver.cancel();
  reduced.addEventListener('change', motionChanged);
  view.addEventListener('pagehide', pageHidden);
  return {
    ...driver,
    destroy() {
      driver.destroy();
      reduced.removeEventListener('change', motionChanged);
      view.removeEventListener('pagehide', pageHidden);
      painter.destroy();
    },
  };
}

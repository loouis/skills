/*
 * SCROLL STORYBOARD — progress follows the viewport, never elapsed time.
 *
 *   0%  Panel top reaches 78% of viewport; inset 24px, top corners 20px.
 * 0–100%  Incoming panel covers the sticky previous section.
 *         A neutral overlay dims the previous section from 0% to 18%.
 *         Only the empty background expands. Content scrolls naturally.
 * 100%  Panel top reaches 6% of viewport; inset 0px, top corners 0px.
 *         Scrolling back reverses the same geometry without a new trigger.
 */
export const DEFAULTS = Object.freeze({
  inset: 24,             // Starting side margin in CSS pixels.
  radius: 20,            // Starting top corner radius in CSS pixels.
  backdropOpacity: 0.18, // Maximum dimming of the section underneath.
  startViewport: 0.78,   // Panel top at animation start, as viewport fraction.
  endViewport: 0.06,     // Panel top at animation end, as viewport fraction.
  reduced: false,        // Preview only; cannot override a system preference.
});

const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
const smoothstep = progress => progress * progress * (3 - 2 * progress);

export function mountExpandingPanel(stage, onUpdate = () => {}) {
  const panel = stage.querySelector('[data-panel]');
  const surface = panel.querySelector('[data-surface]');
  const content = panel.querySelector('[data-content]');
  const underlay = stage.querySelector('[data-underlay]');
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  const options = { ...DEFAULTS };
  let frame = 0;
  let destroyed = false;

  function render() {
    frame = 0;
    const reduced = preference.matches || options.reduced;
    stage.classList.toggle('is-reduced', reduced);
    const panelRect = panel.getBoundingClientRect();
    const contentRect = content.getBoundingClientRect();
    const start = window.innerHeight * options.startViewport;
    const end = window.innerHeight * options.endViewport;
    const progress = reduced ? 1 : clamp((start - panelRect.top) / (start - end), 0, 1);
    const eased = smoothstep(progress);
    // Preserve room around content even when tuning a large inset on mobile.
    const safeInset = Math.min(options.inset, Math.max(0, (panelRect.width - contentRect.width) / 2 - 8));
    const inset = safeInset * (1 - eased);
    const radius = options.radius * (1 - eased);
    const backdropOpacity = reduced ? 0 : options.backdropOpacity * eased;
    surface.style.setProperty('--panel-inset', `${inset.toFixed(3)}px`);
    surface.style.setProperty('--panel-radius', `${radius.toFixed(3)}px`);
    underlay?.style.setProperty('--backdrop-opacity', backdropOpacity.toFixed(4));
    onUpdate({ progress, inset, radius, backdropOpacity, reduced });
  }

  function schedule() {
    if (!destroyed && !frame) frame = requestAnimationFrame(render);
  }

  stage.classList.add('motion-ready');
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule, { passive: true });
  window.addEventListener('pageshow', schedule);
  preference.addEventListener('change', schedule);
  const observer = new ResizeObserver(schedule);
  observer.observe(stage);
  observer.observe(content);
  document.fonts.ready.then(schedule);
  render();

  return {
    update(next) {
      if (destroyed) return;
      for (const key of ['inset', 'radius', 'backdropOpacity', 'startViewport', 'endViewport']) {
        if (Number.isFinite(next[key])) options[key] = next[key];
      }
      options.inset = clamp(options.inset, 0, 160);
      options.radius = clamp(options.radius, 0, 96);
      options.backdropOpacity = clamp(options.backdropOpacity, 0, 1);
      options.startViewport = clamp(options.startViewport, 0.1, 1);
      options.endViewport = clamp(options.endViewport, 0, options.startViewport - 0.05);
      if (typeof next.reduced === 'boolean') options.reduced = next.reduced;
      schedule();
    },
    goTo(progress) {
      const reduced = preference.matches || options.reduced;
      const viewportPosition = options.startViewport + (options.endViewport - options.startViewport) * clamp(progress, 0, 1);
      window.scrollTo({
        top: Math.max(0, window.scrollY + panel.getBoundingClientRect().top - window.innerHeight * viewportPosition),
        behavior: reduced ? 'instant' : 'smooth',
      });
    },
    destroy() {
      destroyed = true;
      cancelAnimationFrame(frame);
      window.removeEventListener('scroll', schedule);
      window.removeEventListener('resize', schedule);
      window.removeEventListener('pageshow', schedule);
      preference.removeEventListener('change', schedule);
      observer.disconnect();
      stage.classList.remove('motion-ready', 'is-reduced');
      surface.style.removeProperty('--panel-inset');
      surface.style.removeProperty('--panel-radius');
      underlay?.style.removeProperty('--backdrop-opacity');
    },
  };
}

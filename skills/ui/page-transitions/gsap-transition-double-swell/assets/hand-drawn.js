// Generated from assets/core by scripts/build-bundle.mjs.
(() => {
'use strict';
// This package's selected default. The shared engine accepts every named variant.
const DEFAULT_VARIANT = 'double-swell';

// Exact six original study geometries. Provenance: ../../references/provenance.md
// Coordinates and stroke widths are normalized to a 1000 × 1000 desktop canvas.
const SHAPES = [
  {
    id: 'wave', name: 'Tidal sweep',
    description: 'One broad S-curve rolls from top to bottom.',
    start: [-160, 160],
    curves: [
      [120, 160, 900, -80, 980, 220],
      [1060, 520, 80, 400, 90, 730],
      [100, 1060, 1040, 1110, 1160, 740],
    ],
    initialStroke: 65, coverStroke: 800, drawnAtCover: 0.85,
    scale: 1, offset: 0,
  },
  {
    id: 'wide-tide', name: 'Wide tide',
    description: 'Long horizontal sweeps with turns beyond the frame.',
    start: [-180, 80],
    curves: [
      [140, 80, 1120, -80, 1120, 240],
      [1120, 560, -120, 360, -120, 740],
      [-120, 1120, 1060, 1100, 1220, 880],
    ],
    initialStroke: 65, coverStroke: 940, drawnAtCover: 0.85,
    scale: 1, offset: 0,
  },
  {
    id: 'diagonal-tide', name: 'Diagonal tide',
    description: 'A broad S sweeps across the page on a slant.',
    start: [-180, 460],
    curves: [
      [80, 620, 560, -220, 880, 0],
      [1200, 220, 160, 430, 340, 760],
      [520, 1090, 980, 1000, 1220, 640],
    ],
    initialStroke: 65, coverStroke: 880, drawnAtCover: 0.85,
    scale: 1, offset: 0,
  },
  {
    id: 'double-swell', name: 'Double swell',
    description: 'Two rounded waves rise and fall across the screen.',
    start: [-180, 750],
    curves: [
      [-10, 820, 70, 120, 240, 120],
      [410, 120, 360, 900, 545, 900],
      [730, 900, 665, 100, 855, 100],
      [1045, 100, 1110, 700, 1240, 640],
    ],
    initialStroke: 65, coverStroke: 880, drawnAtCover: 0.85,
    scale: 1, offset: 0,
  },
  {
    id: 'signature', name: 'Signature loop',
    description: 'A tilted loop with a long, handwritten flourish.',
    start: [-180, 860],
    curves: [
      [110, 860, 630, 120, 840, 100],
      [1050, 80, 1150, 610, 920, 830],
      [660, 1080, 90, 620, 220, 280],
      [320, 20, 700, 20, 760, 280],
      [820, 540, 700, 1020, 1210, 940],
    ],
    initialStroke: 65, coverStroke: 700, drawnAtCover: 0.85,
    scale: 1, offset: 0,
  },
  {
    id: 'figure-eight', name: 'Figure eight',
    description: 'Two loose loops cross and open across the frame.',
    start: [-160, 720],
    curves: [
      [-40, 720, 20, 260, 180, 220],
      [500, 140, 530, 900, 810, 840],
      [1090, 780, 1100, 180, 800, 160],
      [500, 140, 480, 800, 200, 840],
      [-80, 880, -60, 160, 200, 160],
      [480, 160, 700, 800, 1210, 640],
    ],
    initialStroke: 65, coverStroke: 620, drawnAtCover: 0.85,
    scale: 1, offset: 0,
  }
];

const VARIANTS = [
  { name: 'Suite', id: 'wave' },
  { name: 'Wide Tide', id: 'wide-tide' },
  { name: 'Diagonal Tide', id: 'diagonal-tide' },
  { name: 'Double Swell', id: 'double-swell' },
  { name: 'Signature Loop', id: 'signature' },
  { name: 'Figure Eight', id: 'figure-eight' },
];

// “Suite” is an explicit provisional alias for the source Tidal sweep.
function getShape(name = DEFAULT_VARIANT) {
  const key = name.trim().toLowerCase().replace(/\s+/g, '-');
  const aliases = { suite: 'wave', 'tidal-sweep': 'wave', 'signature-loop': 'signature' };
  const shape = SHAPES.find(shape => shape.id === (aliases[key] ?? key));
  if (!shape) throw new RangeError('Unknown hand-drawn transition: ' + name);
  return structuredClone(shape);
}

const TIMING = Object.freeze({
  drawDuration: 1, thickenAt: 0.25, swapAt: 1, revealDuration: 1.25,
  duration: 2.25, fps: 60,
});

const clamp = value => Math.max(0, Math.min(1, value));
// Quadratic power1.inOut is already applied here. GSAP's clock MUST use ease:none.
const ease = value => {
  const t = clamp(value);
  return t < 0.5 ? 2 * t * t : 1 - 2 * (1 - t) ** 2;
};

function frame(time, shape) {
  const incoming = time >= TIMING.swapAt;
  const thickenAt = shape.thickenAt ?? TIMING.thickenAt;
  const draw = ease(time / TIMING.drawDuration);
  const thicken = ease((time - thickenAt) / (TIMING.swapAt - thickenAt));
  const reveal = ease((time - TIMING.swapAt) / TIMING.revealDuration);
  return {
    incoming,
    start: incoming ? reveal : 0,
    end: incoming ? 1 : draw * shape.drawnAtCover,
    stroke: shape.initialStroke + (shape.coverStroke - shape.initialStroke) * (incoming ? 1 - reveal : thicken),
    visible: time > 0 && time < TIMING.duration,
  };
}

const shapePath = shape =>
  `M${shape.start.join(' ')} ${shape.curves.map(curve => `C${curve.join(' ')}`).join(' ')}`;
const shapeTransform = shape => `translate(${shape.offset} ${shape.offset}) scale(${shape.scale})`;

const PORTRAIT_RATIO = 844 / 390;
// First three values are approved reference widths. Others are conservative
// extensions for this reusable package, validated separately from source parity.
const PORTRAIT_COVER = Object.freeze({
  wave: 1370, 'wide-tide': 1550, 'diagonal-tide': 1370,
  'double-swell': 1950, signature: 1550, 'figure-eight': 1400,
});

function portraitShape(source, width, height, options = {}) {
  if (![width, height].every(value => Number.isFinite(value) && value > 0)) {
    throw new RangeError('Viewport dimensions must be positive finite numbers.');
  }
  const ratio = height / width;
  const cover = options.coverStroke ?? PORTRAIT_COVER[source.id];
  if (!Number.isFinite(cover) || cover <= 0) throw new RangeError('Provide a portrait cover width for custom geometry.');
  // Bake the desktop transform before mapping into the portrait coordinate space.
  const point = (x, y) => [x * source.scale + source.offset, (y * source.scale + source.offset) * ratio];
  return {
    viewportHeight: 1000 * ratio,
    shape: {
      ...source,
      start: point(...source.start),
      curves: source.curves.map(([x1, y1, x2, y2, x3, y3]) => [...point(x1, y1), ...point(x2, y2), ...point(x3, y3)]),
      scale: 1, offset: 0,
      initialStroke: options.initialStroke ?? 110,
      coverStroke: cover * Math.max(1, ratio / PORTRAIT_RATIO),
    },
  };
}


let nextFilterId = 0;
const SVG_NS = 'http://www.w3.org/2000/svg';
const element = (doc, tag, attrs = {}) => {
  const node = doc.createElementNS(SVG_NS, tag);
  for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, String(value));
  return node;
};

// Use one empty overlay per painter. Import transition.css in the host app.
function createPainter(overlay, {
  shape, color = '#202020', portraitMaxWidth = 1024, portrait = {},
} = {}) {
  const doc = overlay.ownerDocument;
  const id = `hand-drawn-rounding-${++nextFilterId}`;
  const revealSvg = element(doc, 'svg', { viewBox: '0 0 1000 1000', preserveAspectRatio: 'none', 'data-drawn-reveal': '' });
  const frontSvg = element(doc, 'svg', { preserveAspectRatio: 'xMidYMid meet', 'data-drawn-front': '' });
  const attrs = { fill: 'none', stroke: color, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', visibility: 'hidden' };
  const reveal = element(doc, 'path', attrs);
  const front = element(doc, 'path', { ...attrs, filter: `url(#${id})` });
  const defs = element(doc, 'defs');
  const filter = element(doc, 'filter', {
    id, filterUnits: 'userSpaceOnUse', x: -200, y: -200, width: 1400,
    'color-interpolation-filters': 'sRGB',
  });
  const blur = element(doc, 'feGaussianBlur', { in: 'SourceGraphic', stdDeviation: 0 });
  filter.append(blur, element(doc, 'feColorMatrix', {
    type: 'matrix', values: '1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 24 -11.5',
  }));
  defs.append(filter);
  frontSvg.append(defs, front);
  revealSvg.append(reveal);
  overlay.append(revealSvg, frontSvg);
  overlay.setAttribute('aria-hidden', 'true');
  reveal.setAttribute('d', shapePath(shape));
  reveal.setAttribute('transform', shapeTransform(shape));
  const revealLength = reveal.getTotalLength();
  let frontLength = 0, adapted, usePortrait = false, time = 0;

  const paint = value => {
    time = value;
    const pose = frame(time, shape);
    overlay.dataset.time = time.toFixed(4);
    overlay.dataset.portrait = String(usePortrait);
    reveal.style.visibility = pose.visible && (!usePortrait || pose.incoming) ? 'visible' : 'hidden';
    reveal.style.strokeWidth = String(pose.stroke);
    reveal.style.strokeDasharray = `${(pose.end - pose.start) * revealLength} ${revealLength + 1}`;
    reveal.style.strokeDashoffset = String(-pose.start * revealLength);
    const leading = frame(time, adapted.shape);
    front.style.visibility = usePortrait && leading.visible && !leading.incoming ? 'visible' : 'hidden';
    front.style.strokeWidth = String(leading.stroke);
    front.style.strokeDasharray = `${leading.end * frontLength} ${frontLength + 1}`;
    blur.setAttribute('stdDeviation', String(Math.min(42, leading.stroke * 0.12)));
  };
  const resize = () => {
    // Measure the actual painted rectangle (also works inside a preview stage).
    const bounds = overlay.getBoundingClientRect();
    const width = Math.max(1, bounds.width), height = Math.max(1, bounds.height);
    usePortrait = width <= portraitMaxWidth && height > width;
    adapted = portraitShape(shape, width, height, portrait);
    frontSvg.setAttribute('viewBox', `0 0 1000 ${adapted.viewportHeight}`);
    filter.setAttribute('height', String(adapted.viewportHeight + 400));
    front.setAttribute('d', shapePath(adapted.shape));
    frontLength = front.getTotalLength();
    paint(time);
  };
  resize();
  const observer = new ResizeObserver(resize);
  observer.observe(overlay);
  return {
    paint, resize,
    destroy() { observer.disconnect(); revealSvg.remove(); frontSvg.remove(); },
  };
}


// Wait for readiness, cancellation, or the timeout; always remove listeners/timers.
// Media errors count as settled so a broken image cannot trap the user behind ink.
function settleWithin(work, signal, timeoutMs = 5000) {
  return new Promise(resolve => {
    let timer;
    const finish = () => { clearTimeout(timer); signal?.removeEventListener('abort', finish); resolve(); };
    if (signal?.aborted) return finish();
    signal?.addEventListener('abort', finish, { once: true });
    timer = setTimeout(finish, timeoutMs);
    Promise.resolve(work).then(finish, finish);
  });
}

function loadUntilCancelled(load, signal) {
  return new Promise((resolve, reject) => {
    const cancel = () => { signal.removeEventListener('abort', cancel); resolve(undefined); };
    if (signal.aborted) return cancel();
    signal.addEventListener('abort', cancel, { once: true });
    Promise.resolve().then(() => load(signal)).then(
      value => { signal.removeEventListener('abort', cancel); resolve(value); },
      error => { signal.removeEventListener('abort', cancel); reject(error); },
    );
  });
}

// Router-independent lifecycle. A session owns its clock, signal and completion.
// Cancelling a tween also settles its promise; kill() alone does not do that.
function createDriver({ gsap, paint, onPhase = () => {}, reducedMotion = () => false }) {
  let active, destroyed = false;
  const begin = externalSignal => {
    if (destroyed) throw new Error('Transition driver was destroyed.');
    active?.cancel();
    const controller = new AbortController();
    const clock = { time: 0 };
    let tween, settleTween, finished = false, revealing = false;
    let motion = !reducedMotion();
    const current = () => active === session && !finished && !controller.signal.aborted;
    const stopTween = result => {
      tween?.kill(); tween = undefined;
      const resolve = settleTween; settleTween = undefined; resolve?.(result);
    };
    const finish = () => {
      if (finished) return;
      finished = true;
      stopTween(false);
      externalSignal?.removeEventListener('abort', cancel);
      if (active === session) { active = undefined; paint(0); onPhase('idle'); }
    };
    const cancel = () => { controller.abort(); finish(); };
    const animate = (to, phase) => new Promise(resolve => {
      if (!current()) return resolve(false);
      if (!motion) { clock.time = to; return resolve(true); }
      onPhase(phase);
      settleTween = resolve;
      tween = gsap.to(clock, {
        time: to, duration: to - clock.time, ease: 'none',
        onUpdate: () => { if (current()) paint(clock.time); },
        onComplete: () => { tween = undefined; settleTween = undefined; resolve(current()); },
      });
    });
    const session = {
      signal: controller.signal,
      current,
      cancel,
      reduce() {
        if (!current()) return;
        motion = false;
        clock.time = revealing ? TIMING.duration : TIMING.swapAt;
        stopTween(true);
        paint(0); onPhase('idle');
      },
      covered: Promise.resolve(false),
      async reveal(ready = Promise.resolve(), timeoutMs = 5000) {
        if (!current() || revealing) return false;
        revealing = true;
        const covered = await session.covered;
        if (!covered || !current()) return false;
        await settleWithin(ready, controller.signal, timeoutMs);
        if (!current()) return false;
        const complete = await animate(TIMING.duration, 'reveal');
        if (current()) finish();
        return complete;
      },
    };
    active = session;
    externalSignal?.addEventListener('abort', cancel, { once: true });
    if (externalSignal?.aborted) cancel();
    paint(0);
    session.covered = animate(TIMING.swapAt, 'cover').then(ok => {
      if (ok && current() && motion) onPhase('hold');
      return ok && current();
    });
    return session;
  };
  return {
    begin,
    cancel() { active?.cancel(); },
    reduce() { active?.reduce(); },
    destroy() { active?.cancel(); destroyed = true; },
    // Start fetching alongside cover. Swap only this session's loaded destination.
    async run({ load, swap, ready = () => Promise.resolve(), signal, timeoutMs = 5000 }) {
      const session = begin(signal);
      try {
        const [destination, covered] = await Promise.all([loadUntilCancelled(load, session.signal), session.covered]);
        if (!covered || !session.current()) return false;
        await swap(destination, session.signal);
        if (!session.current()) return false;
        return await session.reveal(ready(session.signal), timeoutMs);
      } catch (error) {
        const cancelled = session.signal.aborted;
        session.cancel();
        if (cancelled) return false;
        throw error;
      }
    },
  };
}



function visibleMediaReady(doc = document) {
  const height = doc.defaultView?.innerHeight ?? 0;
  const images = [...doc.images].filter(image => {
    const bounds = image.getBoundingClientRect();
    return image.loading !== 'lazy' && bounds.bottom > 0 && bounds.top < height;
  });
  return Promise.all([doc.fonts?.ready, ...images.map(image => image.decode().catch(() => {}))]);
}

// Overlay must live outside the route subtree, under body, with the shared CSS.
// lock() is an optional host-owned scroll/input lock; it returns an unlock callback.
function createTransition({
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

window.HandDrawn = { createTransition, createPainter, createDriver, visibleMediaReady, SHAPES, VARIANTS, getShape, frame, portraitShape, TIMING };
})();

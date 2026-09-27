export const TIMING = Object.freeze({
  drawDuration: 1, thickenAt: 0.25, swapAt: 1, revealDuration: 1.25,
  duration: 2.25, fps: 60,
});

const clamp = value => Math.max(0, Math.min(1, value));
// Quadratic power1.inOut is already applied here. GSAP's clock MUST use ease:none.
const ease = value => {
  const t = clamp(value);
  return t < 0.5 ? 2 * t * t : 1 - 2 * (1 - t) ** 2;
};

export function frame(time, shape) {
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

export const shapePath = shape =>
  `M${shape.start.join(' ')} ${shape.curves.map(curve => `C${curve.join(' ')}`).join(' ')}`;
export const shapeTransform = shape => `translate(${shape.offset} ${shape.offset}) scale(${shape.scale})`;

export const PORTRAIT_RATIO = 844 / 390;
// First three values are approved reference widths. Others are conservative
// extensions for this reusable package, validated separately from source parity.
export const PORTRAIT_COVER = Object.freeze({
  wave: 1370, 'wide-tide': 1550, 'diagonal-tide': 1370,
  'double-swell': 1950, signature: 1550, 'figure-eight': 1400,
});

export function portraitShape(source, width, height, options = {}) {
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

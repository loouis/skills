import { frame, portraitShape, shapePath, shapeTransform } from './geometry.mjs';

let nextFilterId = 0;
const SVG_NS = 'http://www.w3.org/2000/svg';
const element = (doc, tag, attrs = {}) => {
  const node = doc.createElementNS(SVG_NS, tag);
  for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, String(value));
  return node;
};

// Use one empty overlay per painter. Import transition.css in the host app.
export function createPainter(overlay, {
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

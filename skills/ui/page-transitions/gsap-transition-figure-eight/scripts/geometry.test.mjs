import assert from 'node:assert/strict';
import test from 'node:test';
import { SHAPES, VARIANTS, getShape } from '../assets/core/shapes.mjs';
import { frame, portraitShape, PORTRAIT_COVER, TIMING } from '../assets/core/geometry.mjs';

function measure(shape) {
  let start = shape.start, previous = start, length = 0;
  const points = [{ x: start[0], y: start[1], length }];
  for (const [x1, y1, x2, y2, x3, y3] of shape.curves) {
    const [x0, y0] = start;
    for (let i = 1; i <= 400; i++) {
      const t = i / 400, a = 1 - t;
      const x = a ** 3 * x0 + 3 * a * a * t * x1 + 3 * a * t * t * x2 + t ** 3 * x3;
      const y = a ** 3 * y0 + 3 * a * a * t * y1 + 3 * a * t * t * y2 + t ** 3 * y3;
      length += Math.hypot(x - previous[0], y - previous[1]);
      points.push({ x, y, length }); previous = [x, y];
    }
    start = [x3, y3];
  }
  return { points, length };
}

function coverage(shape, height, times, context, portrait = false) {
  const { points, length } = measure(shape);
  // The closest sampled centreline point is farther away than the real curve,
  // making the test conservative. Add a half-grid-diagonal to cover grid cells,
  // plus a 12-unit edge allowance for the portrait blur/threshold and rounding.
  const columns = portrait ? 60 : 120, rows = Math.ceil(height / (1000 / columns));
  const allowance = Math.hypot(1000 / columns, height / rows) / 2 + (portrait ? 12 : 1);
  let minMargin = Infinity;
  for (const time of times) {
    const pose = frame(time, shape);
    const drawn = points.filter(p => p.length >= length * pose.start && p.length <= length * pose.end);
    for (let col = 0; col <= columns; col++) for (let row = 0; row <= rows; row++) {
      const x = col * 1000 / columns, y = row * height / rows;
      let squared = Infinity;
      for (const point of drawn) squared = Math.min(squared, (x - point.x) ** 2 + (y - point.y) ** 2);
      const margin = pose.stroke / 2 - Math.sqrt(squared);
      minMargin = Math.min(minMargin, margin);
      assert.ok(margin > allowance, `${context}: uncovered ${x},${y} at ${time}s; margin ${margin}, need ${allowance}`);
    }
  }
  return minMargin;
}

test('all requested names resolve without mutating source geometry', () => {
  for (const { name, id } of VARIANTS) assert.equal(getShape(name).id, id);
  assert.equal(getShape('Suite').id, 'wave');
  assert.equal(getShape('Tidal sweep').id, 'wave');
  getShape('Suite').curves[0][0] = 999;
  assert.equal(getShape('wave').curves[0][0], 120);
  assert.throws(() => getShape('missing'), RangeError);
});

test('every desktop curve covers the handoff and clears both offscreen ends', () => {
  for (const shape of SHAPES) {
    coverage(shape, 1000, [59 / 60, 1, 61 / 60], shape.id);
    assert.ok(shape.start[0] + shape.initialStroke / 2 < 0);
    assert.ok(shape.curves.at(-1)[4] - shape.initialStroke / 2 > 1000);
  }
});

test('all portrait variants cover short, tall, tablet and rotated viewports', () => {
  const sizes = [[320,568],[390,844],[430,932],[360,1000],[320,1200],[768,1024],[1024,1366],[844,390],[1000,1000]];
  for (const source of SHAPES) for (const [width, height] of sizes) {
    const { shape, viewportHeight } = portraitShape(source, width, height);
    assert.ok(Math.abs(viewportHeight / 1000 - height / width) < 1e-12);
    assert.equal(shape.initialStroke, 110);
    coverage(shape, viewportHeight, [59 / 60, 1], `${source.id} ${width}x${height}`, true);
  }
});

test('approved portrait widths and normalized mobile geometry stay exact', () => {
  for (const id of ['wave', 'wide-tide', 'diagonal-tide']) {
    const source = getShape(id), { shape } = portraitShape(source, 390, 844);
    assert.equal(shape.coverStroke, PORTRAIT_COVER[id]);
    for (let i = 0; i < shape.curves.length; i++) for (let j = 0; j < 6; j++) {
      assert.equal(shape.curves[i][j], source.curves[i][j] * (j % 2 ? 844 / 390 : 1));
    }
  }
  assert.throws(() => portraitShape(getShape(), 0, 844), RangeError);
});

test('clock overlaps draw/thicken, swaps deterministically and carries tail forward', () => {
  for (const shape of SHAPES) {
    const poses = Array.from({ length: 136 }, (_, i) => frame(i / 60, shape));
    const overlap = frame(.5, shape);
    assert.equal(overlap.end, .425);
    assert.ok(overlap.stroke > shape.initialStroke && overlap.stroke < shape.coverStroke);
    assert.equal(frame(.25, shape).stroke, shape.initialStroke);
    assert.equal(frame(1, shape).stroke, shape.coverStroke);
    for (let i = 1; i < poses.length; i++) {
      assert.ok(poses[i].start >= poses[i - 1].start);
      assert.ok(poses[i].end >= poses[i - 1].end);
      assert.ok(poses[i].start <= poses[i].end);
      if (i > 60) assert.ok(poses[i].stroke <= poses[i - 1].stroke);
    }
    for (const t of [1.001, .999, 1, 0, 2.25]) assert.equal(frame(t, shape).incoming, t >= 1);
    assert.equal(poses[0].visible, false);
    assert.equal(frame(TIMING.duration, shape).visible, false);
    assert.equal(poses.at(-1).start, poses.at(-1).end);
  }
});

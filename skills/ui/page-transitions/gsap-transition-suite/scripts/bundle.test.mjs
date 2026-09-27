import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';
import test from 'node:test';
import { getShape, VARIANTS } from '../assets/core/shapes.mjs';
import { frame } from '../assets/core/geometry.mjs';

test('standalone browser bundle exposes the selected default and exact frame output', () => {
  const window = {};
  runInNewContext(readFileSync(new URL('../assets/hand-drawn.js', import.meta.url), 'utf8'), { window, structuredClone });
  const api = window.HandDrawn;
  assert.equal(api.getShape().id, getShape().id);
  assert.equal(typeof api.createTransition, 'function');
  for (const variant of VARIANTS) for (const t of [0, .25, .5, 59/60, 1, 61/60, 1.5, 2.25]) {
    assert.deepEqual(JSON.parse(JSON.stringify(api.frame(t, api.getShape(variant.name)))), frame(t, getShape(variant.id)));
  }
});

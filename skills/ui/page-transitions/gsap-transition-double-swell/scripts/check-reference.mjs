import assert from 'node:assert/strict';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
import { SHAPES } from '../assets/core/shapes.mjs';
import { frame } from '../assets/core/geometry.mjs';
if (!process.argv[2]) throw new Error('Usage: node --experimental-strip-types scripts/check-reference.mjs <original-shape-module.ts>');
const { SPIRAL_SHAPES, oSpiralFrame } = await import(pathToFileURL(resolve(process.argv[2])).href);
for (const shape of SHAPES) {
  const original = SPIRAL_SHAPES.find(candidate => candidate.id === shape.id);
  assert.deepEqual(shape, original);
  for (let i = 0; i <= 1350; i++) assert.deepEqual(frame(i / 600, shape), oSpiralFrame(i / 600, original));
}
console.log('Exact source parity: six curve definitions and 8,106 timing poses.');

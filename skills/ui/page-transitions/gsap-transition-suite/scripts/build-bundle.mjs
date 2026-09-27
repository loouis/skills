// Build the classic browser bundle for file:// demos and non-bundled sites.
import { readFileSync, writeFileSync } from 'node:fs';
const asset = new URL('../assets/', import.meta.url);
const modules = ['config', 'shapes', 'geometry', 'painter', 'driver', 'transition'];
const bodies = modules.map(name => readFileSync(new URL(`core/${name}.mjs`, asset), 'utf8')
  .replace(/^import .+;\n/gm, '')
  .replace(/^export \{.+\} from .+;\n/gm, '')
  .replace(/^export /gm, ''));
const bundle = `// Generated from assets/core by scripts/build-bundle.mjs.\n(() => {\n'use strict';\n${bodies.join('\n')}\nwindow.HandDrawn = { createTransition, createPainter, createDriver, visibleMediaReady, SHAPES, VARIANTS, getShape, frame, portraitShape, TIMING };\n})();\n`;
const output = new URL('hand-drawn.js', asset);
if (process.argv.includes('--check')) {
  if (readFileSync(output, 'utf8') !== bundle) throw new Error('Browser bundle is stale; run scripts/build-bundle.mjs');
  console.log('Browser bundle matches core');
} else {
  writeFileSync(output, bundle);
  console.log('Built assets/hand-drawn.js');
}

// Exact six original study geometries. Provenance: ../../references/provenance.md
// Coordinates and stroke widths are normalized to a 1000 × 1000 desktop canvas.
import { DEFAULT_VARIANT } from './config.mjs';
export const SHAPES = [
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

export const VARIANTS = [
  { name: 'Suite', id: 'wave' },
  { name: 'Wide Tide', id: 'wide-tide' },
  { name: 'Diagonal Tide', id: 'diagonal-tide' },
  { name: 'Double Swell', id: 'double-swell' },
  { name: 'Signature Loop', id: 'signature' },
  { name: 'Figure Eight', id: 'figure-eight' },
];

// “Suite” is an explicit provisional alias for the source Tidal sweep.
export function getShape(name = DEFAULT_VARIANT) {
  const key = name.trim().toLowerCase().replace(/\s+/g, '-');
  const aliases = { suite: 'wave', 'tidal-sweep': 'wave', 'signature-loop': 'signature' };
  const shape = SHAPES.find(shape => shape.id === (aliases[key] ?? key));
  if (!shape) throw new RangeError('Unknown hand-drawn transition: ' + name);
  return structuredClone(shape);
}

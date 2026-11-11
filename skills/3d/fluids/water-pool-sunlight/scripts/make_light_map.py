#!/usr/bin/env python3
"""make_light_map.py : the sunlight map for a pool floor and for the sun rays in the water above it.

Brightness is refracted-ray density. A grid of sun rays enters a rippled water surface from straight above, each ray
is bent by Snell's law and followed down to a flat floor, and the rays landing in each cell are counted. Where ripples
focus the rays the count is high (a bright sliver); where they spread the count is low. Nothing is thresholded and
nothing is tiled: the pattern comes from a few broad ripple trains whose strength varies across the pool.

Two maps are written from the same rays:
  <name>-sharp.png   the ray density, lightly blurred (the slivers)
  <name>-soft.png    the same rays spread wider (the pale glow round the slivers; also what the sun rays follow)
  <name>.json        the scale to multiply the stored value by, statistics, and the spec used
  <name>-preview.png a small 8-bit picture of the sharp map, for a first look

Stored value = density / scale, 16-bit greyscale, density mean 1. Row order suits Blender: v rises with +y.
The map is made for a sun straight overhead; the scene shifts the lookup along the real refracted sun direction.

Needs Python 3 and numpy only (the system Python or the one bundled with Blender).

  python3 make_light_map.py SPEC.json OUT_DIR                  one still map
  python3 make_light_map.py SPEC.json OUT_DIR --frames 1 168   a loop (spec needs "loop": {"frames": N}), <name>/sharp-0001.png ...
  python3 make_light_map.py SPEC.json OUT_DIR --train 2        only ripple train 2, at full even strength (direction check)
  ... --bins 2048 --photons 11264                              the same spec at another resolution (loops, quick looks)

Spec (lengths in millimetres):
  name, domain [x0, y0, size], depth, bins, photons, blur_mm, soft_blur_mm, seed, scale, margin,
  trains: [{lam, dir, q | amp, warp, warp_len, base, groups: [[cx, cy, sigma, gain], ...], cycles, wcycles}]
See references/method.md for what each number does.
"""
import argparse
import json
import math
import os
import struct
import sys
import zlib

import numpy as np

N_WATER = 1.333


def amp_from_q(q, lam, depth):
    """Ripple height (mm) that gives focusing strength q at this depth: q = depth * (1 - 1/n) * amp * k^2."""
    k = 2 * math.pi / lam
    return q / ((1.0 - 1.0 / N_WATER) * depth * k * k)


def resolve_trains(spec):
    """Fill in each train's amplitude (from q) and its random phases. Phases are drawn first, in train order."""
    rng = np.random.default_rng(spec.get('seed', 1))
    depth = float(spec.get('depth', 700.0))
    trains = []
    for tr in spec['trains']:
        tr = dict(tr)
        if 'amp' not in tr:
            if 'q' not in tr:
                raise SystemExit('each train needs "q" (focusing strength) or "amp" (height in mm)')
            tr['amp'] = amp_from_q(float(tr['q']), float(tr['lam']), depth)
        tr.setdefault('ph', float(rng.uniform(0, 2 * math.pi)))
        tr.setdefault('wph', float(rng.uniform(0, 2 * math.pi)))
        trains.append(tr)
    return trains, rng


def slopes(x, y, trains):
    """Surface slope (dh/dx, dh/dy) of the summed ripple trains at the points (x, y)."""
    gx = np.zeros_like(x)
    gy = np.zeros_like(x)
    for tr in trains:
        k = 2 * math.pi / tr['lam']
        dx, dy = math.cos(math.radians(tr['dir'])), math.sin(math.radians(tr['dir']))
        # a slow sideways wobble of the phase, so crests bend instead of running ruler-straight
        wk = 2 * math.pi / (tr['lam'] * tr.get('warp_len', 4.0))
        wdx, wdy = -dy, dx
        wa = tr.get('warp', 0.0) * 2 * math.pi
        wph = wk * (wdx * x + wdy * y) + tr['wph']
        w = wa * np.sin(wph)
        dw_x = wa * np.cos(wph) * wk * wdx
        dw_y = wa * np.cos(wph) * wk * wdy
        th = k * (dx * x + dy * y) + tr['ph'] + w
        # height of the train: an even base plus Gaussian groups where the ripples gather (or, with a negative gain, calm)
        A = np.full_like(x, tr['amp'] * tr.get('base', 1.0))
        Ax = np.zeros_like(x)
        Ay = np.zeros_like(x)
        for (cx, cy, sig, gain) in tr.get('groups', []):
            g = tr['amp'] * gain * np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * sig * sig))
            A += g
            Ax += g * (-(x - cx) / (sig * sig))
            Ay += g * (-(y - cy) / (sig * sig))
        s, c = np.sin(th), np.cos(th)
        gx += Ax * s + A * c * (k * dx + dw_x)
        gy += Ay * s + A * c * (k * dy + dw_y)
    return gx, gy


def gauss_blur(a, sigma):
    """Gaussian blur with the edge value repeated outward. Sampled kernel out to 4 sigma."""
    if sigma <= 0:
        return a
    r = int(4.0 * sigma + 0.5)
    x = np.arange(-r, r + 1, dtype=np.float64)
    w = np.exp(-0.5 * (x / sigma) ** 2)
    w /= w.sum()
    for axis in (0, 1):
        pad = [(r, r) if i == axis else (0, 0) for i in range(2)]
        p = np.pad(a, pad, mode='edge')
        out = np.zeros_like(a)
        n = a.shape[axis]
        for i, wi in enumerate(w):
            sl = [slice(None), slice(None)]
            sl[axis] = slice(i, i + n)
            out += wi * p[tuple(sl)]
        a = out
    return a


def write_png_gray(path, a, bits):
    """Greyscale PNG, 8 or 16 bits, written with zlib only. `a` holds integers already in range."""
    h, w = a.shape
    bpp = 2 if bits == 16 else 1
    raw = np.frombuffer(a.astype('>u2' if bits == 16 else 'u1').tobytes(), np.uint8).reshape(h, w * bpp)
    data = np.empty((h, w * bpp + 1), np.uint8)
    data[:, 0] = 1                                   # PNG row filter 'Sub': each byte minus the one a pixel to its left
    data[:, 1:] = raw
    data[:, 1 + bpp:] -= raw[:, :-bpp]

    def chunk(tag, payload):
        return struct.pack('>I', len(payload)) + tag + payload + struct.pack('>I', zlib.crc32(tag + payload) & 0xffffffff)

    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, bits, 0, 0, 0, 0)))
        f.write(chunk(b'IDAT', zlib.compress(data.tobytes(), 6)))
        f.write(chunk(b'IEND', b''))


def trace(spec, trains, rng):
    """Count the refracted rays landing in each floor cell. Returns the density, mean 1 away from the edges."""
    x0, y0, size = spec['domain']
    depth = float(spec.get('depth', 700.0))
    bins = int(spec.get('bins', 4096))
    n = int(spec.get('photons', 14336))
    margin = float(spec.get('margin', 200.0))
    span = size + 2 * margin
    step = span / n
    hist = np.zeros(bins * bins, dtype=np.float64)
    rows = 192
    eta = 1.0 / N_WATER
    for r0 in range(0, n, rows):
        r1 = min(n, r0 + rows)
        xx, yy = np.meshgrid(x0 - margin + (np.arange(n) + 0.5) * step, y0 - margin + (np.arange(r0, r1) + 0.5) * step)
        xx = xx + rng.uniform(-0.5, 0.5, xx.shape) * step
        yy = yy + rng.uniform(-0.5, 0.5, yy.shape) * step
        gx, gy = slopes(xx, yy, trains)
        # surface normal (-gx, -gy, 1), sun ray travelling straight down (0, 0, -1), Snell's law
        inv = 1.0 / np.sqrt(gx * gx + gy * gy + 1.0)
        nx, ny, cosi = -gx * inv, -gy * inv, inv
        kk = 1 - eta * eta * (1 - cosi * cosi)
        f = eta * cosi - np.sqrt(np.maximum(kk, 0))
        tx, ty, tz = f * nx, f * ny, -eta + f * cosi
        fx = xx + depth * tx / -tz
        fy = yy + depth * ty / -tz
        bu = np.floor((fx - x0) / size * bins).astype(np.int64)
        bv = np.floor((fy - y0) / size * bins).astype(np.int64)
        ok = (bu >= 0) & (bu < bins) & (bv >= 0) & (bv < bins)
        hist += np.bincount((bv[ok] * bins + bu[ok]).ravel(), minlength=bins * bins)
    hist = hist.reshape(bins, bins)
    hist /= hist[bins // 8: -bins // 8, bins // 8: -bins // 8].mean()
    return hist


def encode16(a, scale):
    return (np.clip(np.flipud(a) / scale, 0, 1) * 65535).astype(np.uint16)   # file row 0 = largest y


def blur_bins(spec):
    """Blur widths in cells. Given in millimetres so the look does not change with the map's resolution."""
    cell = spec['domain'][2] / float(spec.get('bins', 4096))
    return spec.get('blur_mm', 1.27) / cell, spec.get('soft_blur_mm', 8.8) / cell


def make_still(spec, out_dir, only_train=None, force=False):
    trains, rng = resolve_trains(spec)
    name = spec['name']
    if only_train is not None:
        tr = dict(trains[only_train], base=1.0, groups=[])
        trains = [tr]
        name = f'{name}-train{only_train}'
    paths = {k: os.path.join(out_dir, f'{name}{s}') for k, s in
             (('sharp', '-sharp.png'), ('soft', '-soft.png'), ('json', '.json'), ('preview', '-preview.png'))}
    if not force and any(os.path.exists(p) for p in paths.values()):
        raise SystemExit(f'{name}: output already exists in {out_dir} (use --force to replace it)')
    os.makedirs(out_dir, exist_ok=True)
    raw = trace(spec, trains, rng)
    sb, ss = blur_bins(spec)
    sharp = gauss_blur(raw, sb)
    soft = gauss_blur(raw, ss)
    scale = float(spec.get('scale', 64.0))
    write_png_gray(paths['sharp'], encode16(sharp, scale), 16)
    write_png_gray(paths['soft'], encode16(soft, scale), 16)
    bins = sharp.shape[0]
    f = max(1, bins // 1024)
    small = np.flipud(sharp)[:bins // f * f, :bins // f * f].reshape(bins // f, f, bins // f, f).mean((1, 3))
    write_png_gray(paths['preview'], (np.clip(small / 4.0, 0, 1) ** 0.6 * 255).astype(np.uint8), 8)
    info = {'name': name, 'domain': spec['domain'], 'depth': spec.get('depth', 700.0), 'scale': scale,
            'mean': float(sharp.mean()), 'p50': float(np.percentile(sharp, 50)), 'p90': float(np.percentile(sharp, 90)),
            'p99': float(np.percentile(sharp, 99)), 'p999': float(np.percentile(sharp, 99.9)), 'max': float(sharp.max()),
            'soft_p50': float(np.percentile(soft, 50)), 'soft_p99': float(np.percentile(soft, 99)), 'soft_max': float(soft.max()),
            'files': {'sharp': os.path.basename(paths['sharp']), 'soft': os.path.basename(paths['soft'])},
            'spec': dict(spec, trains=trains)}
    with open(paths['json'], 'w') as fh:
        json.dump(info, fh, indent=1)
    return info


def loop_frames(spec):
    lp = spec.get('loop')
    if not lp or int(lp.get('frames', 0)) < 2:
        raise SystemExit('a loop needs "loop": {"frames": N} in the spec')
    for i, tr in enumerate(spec['trains']):
        for key in ('cycles', 'wcycles'):
            v = tr.get(key, 1 if key == 'cycles' else 0)
            if int(v) != v:
                raise SystemExit(f'train {i}: "{key}" must be a whole number, or the last frame will not meet the first')
    return int(lp['frames'])


def make_frame(job):
    spec, out_dir, frame, force = job
    frames = loop_frames(spec)
    trains, rng = resolve_trains(spec)
    folder = os.path.join(out_dir, spec['name'])
    os.makedirs(folder, exist_ok=True)
    p_sharp = os.path.join(folder, f'sharp-{frame:04d}.png')
    p_soft = os.path.join(folder, f'soft-{frame:04d}.png')
    if not force and os.path.exists(p_sharp) and os.path.exists(p_soft):
        return frame, 'kept'
    # every train moves on by a whole number of its own wavelengths over the loop; the groups and the ray jitter stay
    # put, so only the ripples travel and frame N + 1 would equal frame 1
    u = (frame - 1) / float(frames)
    moved = [dict(tr, ph=tr['ph'] - 2 * math.pi * int(tr.get('cycles', 1)) * u,
                  wph=tr['wph'] + 2 * math.pi * int(tr.get('wcycles', 0)) * u) for tr in trains]
    raw = trace(spec, moved, rng)
    sb, ss = blur_bins(spec)
    scale = float(spec.get('scale', 64.0))
    write_png_gray(p_sharp, encode16(gauss_blur(raw, sb), scale), 16)
    write_png_gray(p_soft, encode16(gauss_blur(raw, ss), scale), 16)
    if frame == 1:
        with open(os.path.join(folder, 'loop.json'), 'w') as fh:
            json.dump({'name': spec['name'], 'domain': spec['domain'], 'depth': spec.get('depth', 700.0), 'scale': scale,
                       'frames': frames, 'spec': dict(spec, trains=trains)}, fh, indent=1)
    return frame, 'made'


def main(argv=None):
    ap = argparse.ArgumentParser(description='Ray-density sunlight map for a pool floor and its sun rays.')
    ap.add_argument('spec')
    ap.add_argument('out_dir')
    ap.add_argument('--frames', nargs=2, type=int, metavar=('FIRST', 'LAST'), help='make loop frames FIRST..LAST')
    ap.add_argument('--jobs', type=int, default=4, help='loop frames made at once (each needs about 2 GB at 4096 cells)')
    ap.add_argument('--train', type=int, help='make only this ripple train (0-based), at full even strength')
    ap.add_argument('--bins', type=int, help='cells along a side, instead of the spec\'s')
    ap.add_argument('--photons', type=int, help='rays along a side, instead of the spec\'s')
    ap.add_argument('--force', action='store_true', help='replace existing output')
    a = ap.parse_args(argv)
    with open(a.spec) as fh:
        spec = json.load(fh)
    if a.bins:
        spec['bins'] = a.bins
    if a.photons:
        spec['photons'] = a.photons
    if a.frames:
        total = loop_frames(spec)
        f0, f1 = a.frames
        if not (1 <= f0 <= f1 <= total):
            raise SystemExit(f'--frames must lie within 1..{total}')
        jobs = [(spec, a.out_dir, f, a.force) for f in range(f0, f1 + 1)]
        if a.jobs > 1 and len(jobs) > 1:
            import multiprocessing as mp
            with mp.get_context('spawn').Pool(a.jobs) as pool:
                for frame, state in pool.imap_unordered(make_frame, jobs):
                    print(f'frame {frame}: {state}', flush=True)
        else:
            for job in jobs:
                print('frame %d: %s' % make_frame(job), flush=True)
    else:
        info = make_still(spec, a.out_dir, a.train, a.force)
        print(json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in info.items() if k != 'spec'}))


if __name__ == '__main__':
    main()

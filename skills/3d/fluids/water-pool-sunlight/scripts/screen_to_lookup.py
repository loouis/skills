"""screen_to_lookup.py : from a pixel in the render to the place in the light map that lights it, and back.

    python3 scripts/screen_to_lookup.py SCENE.json 640,520 300,600      pixels -> floor point and map point
    python3 scripts/screen_to_lookup.py SCENE.json --map -760,1420      map point -> floor point and pixel

Wave groups and wash lobes are placed in map coordinates: where a ray of sunlight entered the water surface. The floor
point it lights sits further along the slanted sun ray, so the two differ by a fixed offset that this script prints.
Point at the pixel where you want the light gathered (or kept quiet) and use the map point it gives.

SCENE.json needs the entries render_demo.py reads (assets/demo-scene.json is one):
  camera.location [x, y, z] mm, camera.lens mm, and camera.pitch_down degrees (looking along +y) or camera.aim [x, y, z]
  pool.depth mm (the floor is flat at z = -depth, the water surface at z = 0), sun_travel [x, y, z], render.size [w, h]
Pixels count from the top-left corner. The camera is taken to be under water, so its rays are straight lines.
Needs numpy only.
"""
import json
import math
import sys

import numpy as np

N_WATER = 1.333
SENSOR = 36.0


def setup(cfg):
    cam = np.array(cfg['camera']['location'], float)
    if 'aim' in cfg['camera']:
        fwd = np.array(cfg['camera']['aim'], float) - cam
    else:
        p = math.radians(cfg['camera']['pitch_down'])
        fwd = np.array([0.0, math.cos(p), -math.sin(p)])
    fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, [0.0, 0.0, 1.0])
    right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    w, h = cfg['render']['size']
    half = (SENSOR / 2) / cfg['camera']['lens']            # tan of half the horizontal angle (sensor fit: width)
    floor_z = -float(cfg['pool']['depth'])

    L = np.array(cfg['sun_travel'], float)
    L /= np.linalg.norm(L)
    horiz = np.array([L[0], L[1], 0.0])
    sin_t = np.linalg.norm(horiz) / N_WATER
    cos_t = math.sqrt(1 - sin_t * sin_t)
    hd = horiz / max(np.linalg.norm(horiz), 1e-12) * sin_t
    shift = hd[:2] * (-floor_z / cos_t)                    # floor point = map point + shift

    def from_pixel(px, py):
        u = (2 * px / w - 1) * half
        v = (1 - 2 * py / h) * half * h / w
        d = fwd + right * u + up * v
        if d[2] >= 0:
            return None, None
        f = cam + d * ((floor_z - cam[2]) / d[2])
        return f, f[:2] - shift

    def from_map(mx, my):
        f = np.array([mx + shift[0], my + shift[1], floor_z])
        r = f - cam
        depth = r @ fwd
        if depth <= 0:
            return f, None
        px = (r @ right / depth / half + 1) * w / 2
        py = (1 - r @ up / depth / (half * h / w)) * h / 2
        return f, (px, py)

    return from_pixel, from_map, shift


def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print(__doc__)
        return
    with open(args[0]) as fh:
        cfg = json.load(fh)
    from_pixel, from_map, shift = setup(cfg)
    print(f'floor point = map point + [{shift[0]:.0f}, {shift[1]:.0f}] mm')
    to_map = True
    for arg in args[1:]:
        if arg == '--map':
            to_map = False
            continue
        a, b = (float(v) for v in arg.split(','))
        if to_map:
            f, m = from_pixel(a, b)
            if f is None:
                print(f'pixel ({a:.0f}, {b:.0f})  looks above the horizon: no floor there')
            else:
                print(f'pixel ({a:.0f}, {b:.0f})  floor [{f[0]:.0f}, {f[1]:.0f}]  map [{m[0]:.0f}, {m[1]:.0f}]')
        else:
            f, p = from_map(a, b)
            where = 'behind the camera' if p is None else f'pixel ({p[0]:.0f}, {p[1]:.0f})'
            print(f'map [{a:.0f}, {b:.0f}]  floor [{f[0]:.0f}, {f[1]:.0f}]  {where}')


if __name__ == '__main__':
    main()

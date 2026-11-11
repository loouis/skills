"""patch_stats.py : how much of a floor patch is fine bright line, and how much is soft light.

    python3 scripts/patch_stats.py RENDER.png@x0,y0,x1,y1 [MORE.png@x0,y0,x1,y1 ...] [--width 1000]

Needs numpy and Pillow (plain Python, not Blender). Give a patch of sunlit floor in pixel coordinates of the picture
as it is; the picture is first resized to --width so numbers from pictures of different sizes can be compared.

  line_frac          share of pixels more than 18 grey levels above their blurred surround (sigma 9 px): fine lines
  strong_frac        the same above 35: the hot centres
  soft_lit_frac      share that is lit but is not a line: the pale glow
  local_contrast_sd  spread of (pixel - surround): how busy the patch is
  soft_sd            spread of the surround itself: how much the broad wash varies across the patch

Use it to compare a change against the picture before it, on the same patch. references/checks.md has the numbers
the demo picture gives and what too wiry looks like in these terms.
"""
import argparse
import json

import numpy as np
from PIL import Image, ImageFilter


def stats(img):
    g = img.convert('L')
    a = np.asarray(g).astype(np.float32)
    soft = np.asarray(g.filter(ImageFilter.GaussianBlur(9))).astype(np.float32)
    exc = a - soft
    line = (exc > 18).mean()
    strong = (exc > 35).mean()
    lit = ((a > np.percentile(a, 20) + 8) & (exc <= 18)).mean()
    return {'mean': round(float(a.mean()), 1), 'line_frac': round(float(line), 4),
            'strong_frac': round(float(strong), 4), 'soft_lit_frac': round(float(lit), 3),
            'local_contrast_sd': round(float(exc.std()), 2), 'soft_sd': round(float(soft.std()), 2)}


def main():
    ap = argparse.ArgumentParser(description='Line and soft-light shares of a floor patch.')
    ap.add_argument('patches', nargs='+', metavar='IMAGE@x0,y0,x1,y1')
    ap.add_argument('--width', type=int, default=1000, help='resize the picture to this width first (0 = leave it)')
    a = ap.parse_args()
    out = {}
    for spec in a.patches:
        path, box = spec.rsplit('@', 1)
        x0, y0, x1, y1 = (int(v) for v in box.split(','))
        img = Image.open(path).convert('RGB')
        if a.width and img.width != a.width:
            k = a.width / img.width
            img = img.resize((a.width, round(img.height * k)), Image.LANCZOS)
            x0, y0, x1, y1 = (round(v * k) for v in (x0, y0, x1, y1))
        out[spec] = stats(img.crop((x0, y0, x1, y1)))   # the path as given: runs share one file name
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()

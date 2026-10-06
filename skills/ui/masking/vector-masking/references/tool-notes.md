# Renderer notes

## SVG / web

Use a separate luminance `<mask>` for each moving piece. White reveals and black hides. An opaque black shape in an **alpha** mask does not hide anything. Set both `maskUnits` and `maskContentUnits` to `userSpaceOnUse`, choose explicit mask bounds covering the motion and overshoot, and use unique IDs when more than one instance appears on a page.

```html
<defs>
  <mask id="mark-back-window"
        maskUnits="userSpaceOnUse" maskContentUnits="userSpaceOnUse"
        x="-100" y="-100" width="800" height="800"
        style="mask-type: luminance">
    <path d="…window…" fill="white" />
    <g transform="…front-piece transform…">
      <path d="…front silhouette including stroke extent…" fill="black" />
    </g>
  </mask>
</defs>
<g mask="url(#mark-back-window)">
  <g transform="…back-piece transform…">
    <path d="…complete piece…" fill="none" stroke="currentColor" />
  </g>
</g>
```

The outer masked group stays in the mark's coordinate system. Only the inner back-piece group moves. The front-copy transform is independent: if it is in a different coordinate space, convert its world transform into mask space. Do not inherit the rear piece's transform or apply the front transform twice.

For an outlined closed shape, the occluder contains its enclosed region plus the visible stroke extent, even when the visible shape has `fill="none"`. Preserve intentional transparent slots. A stroke on the centerline alone is not a silhouette.

### Gap distance and offset geometry

Measure the gap from the **outer painted boundary** of the front stroke. In a centered-stroke renderer, a fill plus a stroke of width `w + 2g` expands the original silhouette outward by `g` when the original width is `w`. Adding only `g` to the centered stroke expands it by `g / 2`. Keep this change on the mask copy, never the visible artwork.

For spatially varying growth, sample the painted boundary in order and compute outward unit normals. Offset a point `p` to `p + n × g × reach(p) × open`. Keep normals consistently outward, including hole orientation; resolve sharp corners, self-intersections and concave regions with a suitable path-offset/boolean operation. A naïve normal shift is suitable only for sufficiently smooth, well-sampled contours. Start from the painted boundary, not the source stroke centerline.

`reach(p)` is 1 at intended gaps and 0 at touching joins, with its transition buried in an area where no visible line touches the mask. Height is a useful parameter only for shapes whose gap regions follow height. On landing, blend any seam underlap out so the final boundary agrees with the source cut ends; an underlap must not reduce the final gap.

About `strokeWidth / 20` of underlap is an initial seam tolerance under an opaque front line, not a universal constant. Tune it at the actual output size. At open slots, use outward clearance instead because no foreground ink can conceal an underlap.

Use a `clipPath` to limit symmetry-line overlap to the narrow strip inside the opposite piece. Do not stack extra masks to compensate for a wrongly solved pose. Fully invisible front pieces must not cut rear lines; re-enable their occluding copies only when their geometry is actually exposed, checking both sides of that change.

### Lines under stroked front pieces

For open-line marks (spokes under rings, strokes under strokes) the cut-out is the front piece's own stroke, drawn narrower, and the window is its fill:

```html
<mask id="m-spoke-0" maskUnits="userSpaceOnUse" maskContentUnits="userSpaceOnUse" x="-60" y="-60" width="160" height="165">
  <path d="OUTER" fill="#fff"/>                                       <!-- window: inside the outer ring's centreline -->
  <path d="OUTER" fill="none" stroke="#000" stroke-width="2.26"/>     <!-- the outer ring's painted silhouette, 0.12 inside its edge (2.5 − 2 × 0.12) -->
  <path d="INNER" fill="#000" stroke="#000" stroke-width="2.26"/>     <!-- the inner ring's silhouette and its hole -->
</mask>
<g mask="url(#m-spoke-0)"><g class="piece"><path d="…the extended line…" fill="none" stroke="currentColor"/></g></g>
<path d="OUTER" fill="none" stroke="currentColor"/><path d="INNER" fill="none" stroke="currentColor"/>   <!-- the rings, painted on top -->
```

The piece is the artwork's line with a straight run added at each end along its own tangent:

```js
const unit = (a, b) => { const l = Math.hypot(b[0] - a[0], b[1] - a[1]); return [(b[0] - a[0]) / l, (b[1] - a[1]) / l]; };
// d: the line's path data. s, p2: its first two points; pe, e: its last two. back, fwd: how far to run on past each end.
function piece(d, s, p2, pe, e, back, fwd) {
  const d0 = unit(s, p2), d1 = unit(pe, e);
  return `M${s[0] - d0[0] * back} ${s[1] - d0[1] * back} L` + d.slice(1) + ` L${e[0] + d1[0] * fwd} ${e[1] + d1[1] * fwd}`;
}
```

With a 2.5-unit stroke and hexagonal rings, 4 units on under the inner ring kept the butt corners inside the ring's band at every angle of a full turn, and 8 units out past the outer ring covered the corners, where the ring's inner edge sits further out than on the flats. Check against the narrowest reach, corners of the butt end included.

A ring that grows with its line weight held, its copies following it:

```js
function ring(el, copies, s, rot = 0) {       // el: the painted ring; copies: its path in every mask, and for the outer ring each window
  const tf = `translate(${cx} ${cy}) rotate(${rot}) scale(${s}) translate(${-cx} ${-cy})`;
  el.setAttribute('transform', tf); el.style.strokeWidth = String(W / s);
  for (const c of copies) { c.setAttribute('transform', tf); if (c.hasAttribute('stroke')) c.setAttribute('stroke-width', String((W - 2 * UNDERLAP) / s)); }
}
```

Two rings as one line: scale the inner ring by `K = outerWidth / innerWidth` so it sits on the outer ring, then ease it to 1 (it contracts and uncovers the lines from the outside in), or ease the outer ring from `1 / K` to 1 (it grows and uncovers them from the inside out).

Threading, one dash the length of the resting piece slid along a track that extends the line far behind it:

```js
// track = piece(…, back: 60, fwd: 4). W = 8 + lineLength + 4 is the piece at rest; D = lineLength + 4 + 2 puts it fully outside at p = 0.
const a0 = 60 - 8 - D * (1 - p);                       // where the dash starts along the track
path.style.strokeDasharray = `${W} ${trackLength + 20}`;
path.style.strokeDashoffset = String(-a0);             // a negative offset moves the dash forward along the path
```

Draw-on gated by the junction, so a line never reaches a ring that is not painted yet:

```js
const a = arcPosNear(outer, outerLength, lineStart) + 1.6;      // arc position of the junction on the ring, plus a little past it
let tStart = 860;
for (let t = 0; t <= 800; t += 4) if (ease(t / 800) * outerLength >= a) { tStart = t + 60; break; }
```

### A landing check in the page

Render the SVG to a canvas at the last masked frame and at the artwork frame, and count the pixels that differ:

```js
async function snap(svg) {
  const c = svg.cloneNode(true); c.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
  c.querySelectorAll('.ink').forEach(p => { p.setAttribute('fill', 'none'); p.setAttribute('stroke', '#fff'); if (!p.style.strokeWidth) p.setAttribute('stroke-width', '2.5'); });   // CSS variables do not survive serialisation
  c.querySelectorAll('.ghost, .showmask').forEach(p => p.remove());
  c.setAttribute('width', 800); c.setAttribute('height', 812);
  const url = URL.createObjectURL(new Blob([c.outerHTML], { type: 'image/svg+xml' }));
  const img = new Image(); await new Promise((ok, no) => { img.onload = ok; img.onerror = no; img.src = url; });
  const cv = Object.assign(document.createElement('canvas'), { width: 800, height: 812 }), g = cv.getContext('2d');
  g.fillStyle = '#000'; g.fillRect(0, 0, 800, 812); g.drawImage(img, 0, 0); URL.revokeObjectURL(url);
  return g.getImageData(0, 0, 800, 812).data;
}
setT(dur - 1); const A = await snap(svg); setT(dur); const B = await snap(svg);
let diff = 0; for (let k = 0; k < A.length; k += 4) if (Math.abs(A[k] - B[k]) > 40) diff++;
```

A few hundred differing pixels at 800 px, spread along the junctions, is antialiasing; bucket them into 40 px blocks and no block should hold more than a few dozen. Thousands in one place is a shape: a spring not settled, a dash not at full length, a ring a hair off scale.

## After Effects / Lottie

Give each moving piece an inverted alpha track matte built from the front silhouettes. Link the matte copies to the front layers' transforms while keeping the rear content independently movable. Preserve the source line weight, cap style and joins. A filled matte silhouette or an expanded copy of the outline is needed; a thin outline alone will not hide the rear piece's interior crossings.

Use a path offset or expanded matte geometry to open the gap. If using a centered matte stroke, apply the `2g` width rule above. A tapered root gap needs spatially controlled geometry, not a uniform stroke increase. For open-line marks, extend each line layer past both ends and matte it with the front stroke's expanded copy; animate a growing ring's path size (ellipse or rectangle size, or path keyframes) rather than layer scale, so the stroke keeps its width.

Do not assume the exported animation retains every After Effects operation. Bake unsupported expressions or procedural geometry into supported path keyframes, check matte and mask support for the chosen Lottie renderer, and compare exported frames in the actual delivery player. The web demo does not establish Lottie parity.

## Figma stills / storyboards

Build the intended window, subtract the expanded front silhouettes with boolean operations, then use the resulting shape as the piece's mask. Duplicate the source geometry before boolean edits. Make sure the mask type and layer order produce the intended visible region.

Resolve the visible stroke into the occluding silhouette before subtraction; check that any outside stroke used to grow the gap participates in the boolean/mask result. Outline a duplicate or use explicit expanded vector geometry when needed. Keep the original artwork intact. Figma poses can document the construction, but they do not verify the exported animation's interpolation or player behavior.

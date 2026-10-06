# Build notes: SVG masks, offset polygons, the twin strip, frame export

How the model in SKILL.md is built in plain SVG and JavaScript. The patterns are what a real logo build settled on; the numbers are in artwork units unless they say otherwise. Adapt the shapes, keep the structure.

Contents: 1 the stack · 2 one piece and its mask · 3 the cut-out as an offset polygon · 4 flush offsets · 5 the window and the twin strip · 6 per-frame update · 7 choreography · 8 the closed pose · 9 frame export and checks · 10 line marks: a stroke under a stroke · 11 a landing check inside the page

## 1. The stack

Back to front, each moving piece in its own masked group, then the static pieces in front, then (hidden until the end) the original artwork:

```html
<svg viewBox="0 0 1600 900">
  <g class="all">                       <!-- everything that moves; swapped out at the hand-over -->
    <defs> ...one <mask> per piece... </defs>
    <g mask="url(#m-back-left)"><g class="piece" data-p="back-left">  ...paths...  </g></g>
    <g mask="url(#m-front-left)"><g class="piece" data-p="front-left"> ...paths... </g></g>
    ...
    <path d="...heart piece..."/>       <!-- static, in front, no mask -->
    <path d="...top piece..."/>
  </g>
  <g class="orig" style="display:none"> ...the untouched artwork... </g>
</svg>
```

The transform goes on the inner `.piece` group, never on the group that carries the mask, so the mask stays where it is while the piece moves.

## 2. One piece and its mask

```html
<mask id="m-back-left" maskUnits="userSpaceOnUse" x="-300" y="-300" width="840" height="760">
  <path class="m-win" d="M-300 -300H120V460H-300Z" fill="#fff"/>      <!-- the window: this piece's own side -->
  <g clip-path="url(#strip-back-left)">                               <!-- twin strip, inner pieces only (section 5) -->
    <g class="m-twin" fill="#fff"> ...the opposite piece's shapes... </g>
  </g>
  <g fill="#000" stroke="#000">
    <g class="m-front" transform="...">  ...the moving front piece's whole shape...  </g>   <!-- chained copy -->
    <path class="m-cut" d="..."/>                                     <!-- the static front piece, as an offset polygon -->
  </g>
</mask>
```

Order inside the mask matters: window first, white helpers next, black cut-outs last, so nothing white can un-hide what the cut-outs hide. Set the mask's `x/y/width/height` to cover everything the piece can reach; the default region is only slightly larger than the bounding box and clips swings.

Keep the units: `maskUnits="userSpaceOnUse"` so the mask shapes share the artwork's coordinates.

## 3. The cut-out as an offset polygon

Sample the front piece's outline once (offline, in Python or in the page at load) as points with outward unit normals, a base offset and a reach weight:

```js
// [x, y, nx, ny, base, reach] per point, in order along the outline
function cutOut(samples, open, closeAt) {
  const pts = samples.map(([x, y, nx, ny, base, reach]) => {
    const o = base + open * reach * (GAP - base);   // flush at open 0, the logo's gap at open 1
    return `${(x + nx * o).toFixed(2)} ${(y + ny * o).toFixed(2)}`;
  });
  return `M${pts.join("L")}${closeAt}Z`;            // closeAt: a few points that close the polygon away from the piece
}
```

- Sample cubic segments at 20–30 steps each; the normal is the tangent turned 90°, flipped to point away from the shape.
- At a pointed corner, add a few extra points at the corner whose normals turn from one side's normal to the other's (a fan). Without them the offset polygon has a notch at every corner.
- `reach` is 1 above the height where the artwork's gaps are and eases to 0 (a smoothstep over a short span) by the height where lines meet. Put the fade where only the piece's fill meets the front piece, so it is never seen.
- Measure `GAP` from the artwork: the distance from a cut end to the front piece's outline, sampled along the cut end. If it is even (it usually is), one number serves.
- Close the polygon on the far side of the mark's centre line, outside the window, so the closing edges can never show.
- With two sub-shapes in one path, make sure they wind the same way or draw them as two paths; opposite windings cancel where they overlap.

## 4. Flush offsets

`base` is the offset when nothing is open:

- `-0.6` (about a twentieth of an 11.8-unit stroke) along a line of the front piece: the back piece runs that far under the line, so there is solid colour under the line's anti-aliased edge and no seam.
- `+0.3` across an open slot in the front piece, where there is no line to hide under, so the back piece does not poke into the slot.
- When the front piece is well away (hidden behind its own mask, or lowered), treat the slot points as `-0.6` too: there is no slot to bridge yet, and a point pushed outside would cut a sliver out of the back piece.

## 5. The window and the twin strip

The window is the half-plane on the piece's own side. Two pieces that meet on the centre line (the two inner petals of a bud, their tips coming together at the top, their top edges coming down onto the piece in front) need care:

- Cut both exactly on the centre line: no overlap, so no sliver sticks out of the join.
- Let each pass the line, by half a unit, **only where the other piece is**: a `<clipPath>` holding a rect from the centre line half a unit into the other side, around a white copy of the other piece at its current transform. Inside the other piece's shape the two overlap and the seam disappears; outside it, nothing shows.

```html
<clipPath id="strip-front-left"><rect x="120" y="-300" width="0.5" height="760"/></clipPath>
```

While pieces are rising out of the front piece, closed, narrow the window to the space above the front piece's top edge, so their lowered bodies stay out of sight, and shorten the strip's rect to the same height.

## 6. Per-frame update

Keep references to the elements once and set attributes each frame:

```js
function apply(H, st) {
  const turn = n => `translate(${st.shift[n][0]} ${st.shift[n][1]}) rotate(${st.rot[n]} ${PX} ${PY})`;   // PX,PY: the pivot
  for (const n of PIECES) { H.pcs[n].setAttribute("transform", turn(n)); H.pcs[n].style.display = st.shown[n] ? "" : "none"; }
  for (const m of H.masks) {
    m.win.setAttribute("d", windowPath(m.piece, st.pre));
    if (m.twin) m.twin.setAttribute("transform", turn(m.twin.dataset.p));   // the opposite piece's copy follows that piece
    if (m.front) m.front.setAttribute("transform", turn(m.front.dataset.p)); // the chained front copy follows the front piece
    m.cut.setAttribute("d", cutOut(SAMPLES[m.piece], st.open[m.piece], ...));
  }
}
```

At the hand-over (`st.final`) hide `.all` and show `.orig`. Before that, ease every remaining offset to exactly zero (multiply by a "calm" factor that runs 1 → 0 over the last half second), or the swap will jump.

## 7. Choreography

Underdamped spring, as progress 0 → 1 with overshoot:

```js
const spring = (t, w, z) => {           // t seconds since start, w rad/s, z damping (0.5 bouncy, 0.8 nearly none)
  if (t <= 0) return 0;
  const wd = w * Math.sqrt(1 - z * z);
  return 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + (z * w / wd) * Math.sin(wd * t));
};
```

- Piece angle: `rest * (1 - spring(t - start, w, z)) * calm`. Back pieces start first with lower damping (w 6, z 0.62); front pieces a little later (w 6.5, z 0.5).
- The gap: `open = 1 - (1 - spring(t - bounce, 10, 0.7)) * calm`, where `bounce` is the top of the front pieces' swing: `start + π / (w √(1 − z²))`.
- Anything that must not overshoot (a shift that would dip a base below the mark) uses the clamped progress squared instead of the raw spring.
- Pieces that have not started are not drawn (`shown`), so the closed state is exactly the front piece.

## 8. The closed pose

For a piece that closes up against a mirror twin, solve the pose numerically rather than using the resting rotation:

- Turn about the pivot until the piece's own axis (the bisector of its tip's two facets) is upright, then search a few degrees either side.
- For each angle, shift sideways so the inside corner of the tip sits on the centre line, and shift up or down so the outer edge passes through the front piece's corner.
- Measure the angle between the piece's edge and the front piece's edge at that corner (the kink) and how far the piece pokes outside the front piece below it. Pick the angle with no kink and no poke; stop a fraction short of zero kink so the join never opens.

## 9. Frame export and checks

Render stills with one headless Chrome driven over the DevTools protocol (set the page to a `?frame=<key>&t=<seconds>` mode that fills the window with the stage), capture 1600×900 PNGs at 25fps, and make contact sheets with Pillow. Then:

- Closed state: frames with the pieces vs frames with the front piece only must differ by 0 pixels.
- Hand-over: the last masked frame vs the first artwork frame should differ by a few dozen edge pixels at most (anti-aliasing), never by a shape.
- Any switch (a window changing form, a schedule change for reverse): the frames either side must match.
- Zoom sheets of the tip, the joins and the base at 5–20× are where slivers, nicks and crowns show up. Fix the geometry, not the frame.

## 10. Line marks: a stroke under a stroke

The same stack for open lines that pass under rings, or under any stroked front piece. The artwork has no gaps, so there are no offset polygons: the inset is a narrower stroke.

The piece is the artwork's line with a straight run added at each end along its own tangent:

```js
const unit = (a, b) => { const l = Math.hypot(b[0] - a[0], b[1] - a[1]); return [(b[0] - a[0]) / l, (b[1] - a[1]) / l]; };
// d: the line's path data. s, p2: its first two points; pe, e: its last two. back, fwd: how far to run on past each end.
function piece(d, s, p2, pe, e, back, fwd) {
  const d0 = unit(s, p2), d1 = unit(pe, e);
  return `M${s[0] - d0[0] * back} ${s[1] - d0[1] * back} L` + d.slice(1) + ` L${e[0] + d1[0] * fwd} ${e[1] + d1[1] * fwd}`;
}
```

Sizing, from a build with a 2.5-unit stroke and hexagonal rings: 4 units on under the inner ring kept the butt corners inside the ring's band at every angle of a full turn (the band is narrowest across a flat side); 8 units out past the outer ring covered the corners, where the ring's inner edge sits further out than on the flats. Check yours against the narrowest reach, corners of the butt end included.

The mask: the outer ring filled is the window; both rings stroked `w − 2·inset` are the cut-outs; the inner ring is filled as well so its hole is hidden.

```html
<mask id="m-blade-0" maskUnits="userSpaceOnUse" x="-60" y="-60" width="160" height="165">
  <path d="OUTER" fill="#fff"/>                                       <!-- window: inside the outer ring's centreline -->
  <path d="OUTER" fill="none" stroke="#000" stroke-width="2.26"/>     <!-- the outer ring's painted silhouette, 0.12 inside its edge -->
  <path d="INNER" fill="#000" stroke="#000" stroke-width="2.26"/>     <!-- the inner ring's silhouette and its hole -->
</mask>
<g mask="url(#m-blade-0)"><g class="piece"><path d="…the extended blade…" class="ink"/></g></g>
<path d="OUTER" class="ink"/><path d="INNER" class="ink"/>            <!-- the rings, painted on top -->
```

A ring that grows about the centre with its line weight held, its copies following it:

```js
function ring(el, copies, s, rot = 0) {       // el: the painted ring; copies: its path in every mask (and, for the outer ring, each window)
  const tf = `translate(${cx} ${cy}) rotate(${rot}) scale(${s}) translate(${-cx} ${-cy})`;
  el.setAttribute('transform', tf); el.style.strokeWidth = String(W / s);
  for (const c of copies) { c.setAttribute('transform', tf); if (c.hasAttribute('stroke')) c.setAttribute('stroke-width', String((W - 2 * INSET) / s)); }
}
```

Two rings as one line: scale the inner ring by `K = outerWidth / innerWidth` so it sits on the outer ring, then ease it to 1 (the ring contracts and uncovers the lines from the outside in), or ease the outer ring from `1 / K` to 1 (it grows and uncovers them from the inside out). The corner radii differ a little; at a tenth of a stroke it does not show.

Threading: one dash the length of the resting piece, slid along a track that extends the line far behind it:

```js
// track = piece(…, back: 60, fwd: 4). W = 8 + lineLength + 4 is the piece at rest; D = lineLength + 4 + 2 puts it fully outside at p = 0.
const a0 = 60 - 8 - D * (1 - p);                       // where the dash starts along the track
path.style.strokeDasharray = `${W} ${trackLength + 20}`;
path.style.strokeDashoffset = String(-a0);             // a negative offset moves the dash forward along the path
```

Draw-on gated by the junction: start each line once the front ring's drawing end is past where they meet.

```js
const a = arcPosNear(outer, outerLength, lineStart) + 1.6;      // arc position of the junction on the ring, plus a little past it
let tStart = 860;
for (let t = 0; t <= 800; t += 4) if (ease(t / 800) * outerLength >= a) { tStart = t + 60; break; }
```

Order the schedule so the ring at the far end is fully drawn before the first line reaches it, and put the drawing head in the same mask as the lines.

## 11. A landing check inside the page

No headless browser needed: render the SVG to a canvas at the last masked frame and at the artwork frame, and count the pixels that differ.

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

What to expect: a few hundred pixels at 800 px, spread along the junctions, is anti-aliasing. Bucket the differing pixels into 40 px blocks; no block should hold more than a few dozen. Thousands in one place is a shape: a spring not settled, a dash not at full length, a ring a hair off scale. Run it on every variation, not just one; identical counts across variations are a good sign that they all reach the same landed state.

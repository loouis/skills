# Build notes: SVG masks, offset polygons, the twin strip, frame export

How the model in SKILL.md is built in plain SVG and JavaScript. The patterns are what a real logo build settled on; the numbers are in artwork units unless they say otherwise. Adapt the shapes, keep the structure.

Contents: 1 the stack · 2 one piece and its mask · 3 the cut-out as an offset polygon · 4 flush offsets · 5 the window and the twin strip · 6 per-frame update · 7 choreography · 8 the closed pose · 9 frame export and checks

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

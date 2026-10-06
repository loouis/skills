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

## After Effects / Lottie

Give each moving piece an inverted alpha track matte built from the front silhouettes. Link the matte copies to the front layers' transforms while keeping the rear content independently movable. Preserve the source line weight, cap style and joins. A filled matte silhouette or an expanded copy of the outline is needed; a thin outline alone will not hide the rear piece's interior crossings.

Use a path offset or expanded matte geometry to open the gap. If using a centered matte stroke, apply the `2g` width rule above. A tapered root gap needs spatially controlled geometry, not a uniform stroke increase.

Do not assume the exported animation retains every After Effects operation. Bake unsupported expressions or procedural geometry into supported path keyframes, check matte and mask support for the chosen Lottie renderer, and compare exported frames in the actual delivery player. The web demo does not establish Lottie parity.

## Figma stills / storyboards

Build the intended window, subtract the expanded front silhouettes with boolean operations, then use the resulting shape as the piece's mask. Duplicate the source geometry before boolean edits. Make sure the mask type and layer order produce the intended visible region.

Resolve the visible stroke into the occluding silhouette before subtraction; check that any outside stroke used to grow the gap participates in the boolean/mask result. Outline a duplicate or use explicit expanded vector geometry when needed. Keep the original artwork intact. Figma poses can document the construction, but they do not verify the exported animation's interpolation or player behavior.

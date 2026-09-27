# Motion and viewport contract

## Variant parameters

| Requested name | Stable source ID | Desktop start → cover | Portrait start → cover at 390 × 844 |
| --- | --- | --- | --- |
| Suite (assumed Tidal sweep) | `wave` | 65 → 800 | 110 → 1370 |
| Wide Tide | `wide-tide` | 65 → 940 | 110 → 1550 |
| Diagonal Tide | `diagonal-tide` | 65 → 880 | 110 → 1370 |
| Double Swell | `double-swell` | 65 → 880 | 110 → 1950 |
| Signature Loop | `signature` | 65 → 700 | 110 → 1550 |
| Figure Eight | `figure-eight` | 65 → 620 | 110 → 1400 |

“Suite” is the user's supplied label; there is no source curve with that name. It provisionally aliases Tidal sweep (`wave`). State this when it matters, and keep the alias easy to change if clarified. Do not rename the stable source ID. All six exact cubic paths are in `assets/core/shapes.mjs`; `getShape()` accepts the requested names and IDs and returns a deep copy.

The first three portrait widths are from the approved mobile reference. The final three are new conservative extensions, not claims of approved mobile parity. They use the same rounded-front treatment and pass the bundled coverage matrix. All six desktop paths and stroke parameters match the source.

## Choreography

- 0–1s: draw from zero to 85% of a single path.
- 0.25–1s: overlap drawing with quadratic stroke expansion.
- 1s: fully opaque cover. Swap the page and extend the concealed end to 100%.
- 1–2.25s: advance the tail from 0 to 100%, thinning to the initial width.
- Slow resources can extend only the full-cover hold. The reference comparison's 0.9s pauses are not part of navigation.

`frame()` matches the source pure renderer. It already applies quadratic `power1.inOut`; animate its time linearly with `ease: 'none'`. Never add a second ease, collapse the curve into a dot, insert a flat background cover, translate it to a new origin at handoff, or reverse the tail. Returning to a previous page uses the same forward gesture with different content, not a reversed clock.

## Portrait front and reveal

Desktop uses a 1000 × 1000 SVG with `preserveAspectRatio="none"`. Its geometry and stroke stretch together, preserving the reference coverage and reveal.

For portrait widths up to 1024px, bake the centreline into `1000 × (1000 * height / width)` before stroking. Use a matching viewBox with uniform SVG scaling: x/y screen scale must be equal, so the leading round cap remains circular. Measure the overlay's actual rectangle, including after orientation or viewport changes.

At the reference 390 × 844 ratio, use the table above. For taller ratios, multiply the portrait cover width by `max(1, actualRatio / (844 / 390))`. Shorter ratios retain the reference cover width. The painter remeasures on `ResizeObserver` updates and repaints the same clock position.

Round the front's overlap joins with isotropic blur `min(42, stroke * 0.12)` and alpha threshold `0 0 0 24 -11.5`. The filter uses a unique ID per painter and a region extending 200 normalized units beyond each viewport edge. Do not apply the filter to the established trailing reveal.

At exactly 1s hide the portrait front and show the original normalized reveal. Both must already be opaque across the entire viewport. The geometry change is concealed by the same continuous ink. No separate fill is used. Full cover also needs an opaque ink color: use a solid CSS color, without alpha/opacity or blend modes.

## Customizing

Color and overlay stacking are independent of the motion. `portraitMaxWidth` changes the responsive cutoff; `Infinity` enables the portrait front on all portrait widths. Pass a deep-copied `shape` and explicit `portrait` stroke options for custom curves. The portrait cover override is calibrated at 390 × 844 and scaled for taller screens.

Changing curves, scales, offsets, draw fraction or cover widths invalidates the source's coverage evidence. Add the custom geometry to the coverage matrix and inspect frames 59–61 before routing real content through it. Preserve default timing unless the user asks for a different rhythm.

The bundled coverage tests sample the actual cubic path and reserve a half-grid-diagonal plus edge margin, checking the grid cells as well as grid points. They cover short/tall phones, tablet, square and rotated dimensions; actual browser pixels and physical devices remain separate checks.

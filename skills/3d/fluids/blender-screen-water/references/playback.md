# Playback and display integration

## Arrival once, repeat the developed flow

Keep `video.loop=false`. Activation starts at zero; an active player's `ended` event seeks to 3 seconds and resumes. Use decoded frame 91 as the poster or reduced-motion fallback. `ScreenWaterFilm` accepts explicit movie/poster URLs; it does not import assets or controls from another project.

For deterministic elapsed milliseconds:

```js
const n = Math.floor(Math.max(0, elapsedMs) * 30 / 1000);
const frame = 1 + (n < 180 ? n : 90 + (n - 180) % 90);
```

Use the encoder's decoded frames so the final 0.6-second blend survives. Whole-file looping, modulo 6 seconds or ping-pong playback changes the intended arrival/repeat. HTML video seeking may pause briefly on some devices; test the actual decoder. For frame-accurate offline rendering use the mapped decoded sequence.

`arrivalOpacity(ms)` is smoothstep over 160 ms. The film adapter token-guards asynchronous play completion, exposes load/playback errors and provides `reset()`/`dispose()`. A consumer should stop/reset decorative playback on focus loss or reduced-motion changes, and dispose it when unmounted. Reduced motion returns the poster.

## Stop state and decorative clearing

Controller state stops immediately. Keep a separate decorative tail alive for 1100 ms so water keeps moving while its mask descends and opacity falls. Do not keep the real device/controller in an active state to finish the visual effect.

For `p=clamp(elapsed/1100,0,1)`, alpha is `1-smoothstep(p)`. At the baseline 480 × 1800:

- Boundary: `-45 + 1890 × p^1.25`.
- Amplitude: `11 × sin(πp)`.
- Wave at x: `amplitude × (sin(x/480 × 6.1 + p × 2) + .28 × sin(x/480 × 12.8))`.
- Keep the region below that boundary, blur the mask by 3.5 px, then composite with alpha.

`drainState()` scales those values to the canvas. Draw a mask covering the lower region on a separate canvas, use `destination-in` on the water layer, and draw sharp interface content afterward. The mask clears the water downward; it does not translate the whole display. Reset obsolete tails on new input.

If using the matching two-control choreography, fade the active caption over 160 ms. Hot returns from 1140 ms and Cold from 1230 ms, each over 660 ms with opacity 0→1 and scale .975→1. `controlReturn()` exposes those values. These are a reusable example, not a requirement to add controls to a water-only task or redesign an existing interface.

## Behind glass

Keep three concerns separate: the water movie, sharp UI, and the consumer display/glass presentation. A flat emissive movie with a surface reflection has no true internal water parallax. Placing it below a real cover adds glass reflections/refraction, but the baked water remains flat imagery.

Use the supplied consumer model in a fresh scene. Fit its existing display and mask, preserve aspect and orientation, and check close/low angles for leaks, z-fighting, stretching and reflections that obscure the water. Do not expand the screen backing or change product geometry merely to hide an integration defect. A real water volume inside that product is separately scoped work. Source-water camera settings do not prescribe a product camera move.

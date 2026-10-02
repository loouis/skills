# Expanding scroll panel — reusable prompt

Use this with the files in this folder as a working reference. The [README](README.md) explains how to run the prototype and how the effect works. This is a prototype prompt; it is not an installed skill yet.

## Short prompt

> Build a scroll section that starts as an inset panel with rounded top corners. As it scrolls upward over the preceding section, expand only its background to the full page width and reduce the corner radius to zero. Keep the text and cards at exactly the same horizontal position and width throughout. Gently dim the preceding section with a grey overlay as the new panel covers it. Reverse the effect when scrolling up. Use only big section headings and cards—no branding, arrows, eyebrows, captions, extra copy or demo controls. Follow the working expanding-scroll-panel prototype for the motion and structure.

## Detailed implementation prompt

```text
Implement the expanding scroll panel effect using this prototype as the reference.
Reuse its controller and CSS structure where possible, adapting the markup to
the receiving project without changing the motion.

Layout and layers
- Put the preceding section and incoming panel inside a shared stage.
- Keep the preceding section sticky while the next panel covers it.
- Give the incoming panel a higher stacking order and a full-width wrapper.
- Place its empty background surface and content container as siblings.
- Only animate the background's side inset and top corner radius. Do not
  scale or animate the width, horizontal padding or margins of the content.
- Text and cards scroll vertically with the page. Their horizontal position,
  dimensions and line wrapping must remain unchanged during expansion.

Motion defaults
- Initially overlap the preceding section by 22% of the small viewport height.
- Start expansion when the incoming panel's top reaches 78% of viewport height.
- Finish when its top reaches 6% of viewport height.
- Animate the side inset from 24px to 0px and top corner radius from 20px to 0px.
- Cap the starting inset on narrow screens to the content gutter minus 8px.
- Use clamped scroll progress with smoothstep easing: p * p * (3 - 2 * p).
- On the preceding section, fade a neutral black overlay from 0 to 18% opacity
  using the same eased progress. Keep it beneath the incoming panel, confined
  to the preceding section, with pointer-events: none.
- Reverse all values directly on upward scroll, with no delayed catch-up,
  scroll locking, time-based entrance animation or independent text animation.

Presentation and accessibility
- Show only large section headings and cards.
- Do not add branding, arrows, eyebrows, captions, supporting copy, footers,
  progress displays or tuning controls unless specifically requested.
- Respect prefers-reduced-motion: use normal document flow, a full-width panel
  and no dimming or sticky overlap. Keep the same readable fallback without JS.
- Recalculate after resizing and content changes. Clean up listeners, observers
  and inline animation styles when unmounting in a client router.

Verification
- Check start, midpoint, full expansion and reverse scroll.
- Confirm the content's x-position, width and line wrapping stay constant.
- Confirm the final inset and radius are zero and only the preceding section dims.
- Check mobile layout, horizontal overflow and reduced-motion behavior.
```

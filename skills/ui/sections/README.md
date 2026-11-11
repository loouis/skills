# Section Skills

Skills for the edges and transitions between page sections. Each gooey section skill makes the boundary between two sections behave like a liquid surface pulled by scroll speed: scrolling down drags the lower section's colour up into the one above, scrolling back up dips the edge the other way, and at rest it's a straight line. They share one engine, a 1:1 port of the original lab, and differ only in feel.

<!-- skills:start -->
| Skill | Use it for |
| --- | --- |
| [Gooey Section: Drift](gooey-section-drift) | Crest that surfs sideways as you scroll |
| [Gooey Section: Elastic](gooey-section-elastic) | Springy edge that overshoots and twangs back |
| [Gooey Section: Goo](gooey-section-goo) | Tight sticky bulge with sinking flanks |
| [Gooey Section: Honey](gooey-section-honey) | Heavy blob: slow rise, very slow droop |
| [Gooey Section: Peel](gooey-section-peel) | Fast drain from full stretch, slow peeling tail |
| [Gooey Section: Slosh](gooey-section-slosh) | Liquid lean: rises one side, dips the other |
| [Gooey Section: Taffy](gooey-section-taffy) | Stretches on scroll, snaps back with one wobble |
| [Gooey Section: Twin](gooey-section-twin) | Main bulge plus a smaller blob beside it |
| [Gooey Section: Wave](gooey-section-wave) | Broad flowing crest pulled by scroll speed |
<!-- skills:end -->

## Use a skill

Copy the complete skill folder into your agent's skills directory, or run `python3 install.py` from the repo root for Claude Code. Then ask for the feel you want:

```text
Use $gooey-section-taffy to add the taffy goo between the sections of this page.
```

```text
Use $gooey-section-honey on the top edge of section_stats in Webflow, and tell me exactly what to paste where.
```

```text
Use $gooey-section-slosh to add the slosh edge between the sections of this Next.js homepage.
```

In Claude Code you can also just describe it ("make the edge between these sections gooey") or type `/gooey-section-goo`. Goo is the default when no feel is named.

Every skill covers plain HTML, Webflow (a custom attribute plus footer code) and React or Next.js. Open a skill's `demo/index.html` to see its feel before using it.

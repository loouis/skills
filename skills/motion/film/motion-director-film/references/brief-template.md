# Brief template

Copy this into `brief.md` at the start of a film. Any line may be left blank: decide it yourself and write the choice next to it with a one-line reason.

```text
mode:        [showreel | product | launch-story | explainer]
subject:     [product URL, topic, or "the craft itself"]
viewer:      [who's watching and what they care about]
end state:   [what they should feel, know or do in the last second]
length:      [e.g. 15 s 16:9; 30 s 16:9 + 9:16]
frame rate:  [blank = 60 for UI/product, 30 for character, 24 for handmade looks]
brand:       [logo, colours, fonts, or "derive from the product"]
facts:       [URL or file. The only source for any claim on screen or in voice.]
assets:      [files, or "capture from the live product"]
style:       [direction or reference videos, or blank]
sound:       [music + sfx | voice + music + sfx | silent]
autonomy:    [unattended: never stop | gated: stop at each ◆]
toolchain:   [Remotion | HTML + GSAP renderer | a kit repo to follow | blank]
sign-off:    [end mark and call to action]
```

## Defaults for blank lines

| Line | Default when blank |
| --- | --- |
| mode | `product` if a product URL is given, `explainer` if a topic is, `showreel` if the subject is the craft |
| length | 15 s 16:9 |
| frame rate | 60 for UI/product, 30 for character work, 24 for handmade looks |
| brand | derive from the product: SVG logo from source, sampled colours and fonts |
| facts | the product's own public pages; if there are none, put no claims on screen |
| assets | capture from the live product |
| sound | music + sfx |
| autonomy | gated |
| toolchain | Remotion for React/UI products, otherwise an HTML + GSAP frame renderer |
| sign-off | the product name and URL |

## Precedence

The brief wins. Then any kit or repo the brief names. Then the skill's defaults.

# Critic loop and quality bar

## Who critiques

The builder never judges its own work. Each review is a fresh critic subagent that has seen none of the building. Give it only the render (or storyboard), the brief, `facts.json`, `timing.json` and the references. It pulls its own frames, measures, and returns problems ranked by severity with timestamps, ending in exactly one verdict: `ship` or `one more pass`.

## When

- After the storyboard.
- After each scene is built.
- After every full render.

## Frame sampling

- A frame every 0.2 s across the film.
- Dense sampling (every frame) for ±0.5 s around every transition and every beat-snapped hit.
- Frame 0 and the last frame, always.

## Extra passes on every full render

1. **Sound-off read**: a critic sees only a silent 2 fps contact sheet and retells the story. If the retelling misses the end state, the picture is not carrying the film.
2. **Sync**: every hit and every voice line lands within 1 frame of `timing.json`.
3. **Fact check**: every word on screen and in voice traces to an entry in `facts.json`.
4. **Director's review**: a blunt critique of what feels assembled, slow or generic, judged against the references.

## Fixing

Fix the biggest problem first, re-render, and have a new critic recheck every earlier item, not only the one you fixed. Log every round in `ledger.md`:

```text
## Round N
- problem (timestamp): before → after (measured value or critic note)
- verdict: ship | one more pass
```

## Quality bar

Measured:

- [ ] Exact duration, size and frame rate (`ffprobe`).
- [ ] Frame one is a finished picture.
- [ ] At most 1 s frozen per 30 s, and no still stretch over 0.5 s (frame-difference pass).
- [ ] Text contrast at least 4.5:1, no collisions, everything inside safe margins.
- [ ] Brand colours match in the encoded render (sample pixels, not the source).
- [ ] Cuts and hits within 1 frame of the beat.
- [ ] Integrated loudness about −14 LUFS, true peak ≤ −1 dBTP, no clipping; effects sit below music and voice.
- [ ] The film is understood with the sound off.
- [ ] Every claim is in `facts.json`, and nothing is invented: no testimonials, ratings, prices, results or real people. Anything generated is labelled.

Judged:

- [ ] A critic would put it beside the references without it looking weaker.

Record each item as pass/fail with its measured number in the quality-bar results.

## Useful measurements

```sh
ffprobe -v error -show_entries stream=width,height,r_frame_rate,nb_frames:format=duration -of json out.mp4
ffmpeg -i out.mp4 -af ebur128=peak=true -f null -          # loudness and true peak
ffmpeg -i out.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null -   # cut detection
ffmpeg -i out.mp4 -vf "fps=2,scale=480:-1,tile=6x5" -frames:v 1 sheet.png   # 2 fps contact sheet
ffmpeg -i out.mp4 -vf "freezedetect=n=0.001:d=0.5" -f null -   # still stretches over 0.5 s
```

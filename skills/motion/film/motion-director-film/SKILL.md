---
name: motion-director-film
description: Directs, animates, scores and QAs a finished short film entirely in code (Remotion or an HTML + GSAP frame renderer, encoded with ffmpeg), from a one-page brief through facts, concept, storyboard, style frames, an audio-first timing map, build, independent critic passes and a measured quality bar. Covers four modes: showreel (the craft is the subject), product (real UI rebuilt as live components), launch-story (characters carry the release) and explainer (one cause and effect, narrated). Use it whenever the user wants a promo, launch video, product film, sizzle reel, showreel, motion piece or animated explainer made in code, rendered to MP4 in one or more aspect ratios, with music, sound effects or voice, or asks to make a video "that holds up next to the best work". Also for reviewing or fixing such a film: sync drift, frozen stretches, unreadable type, invented claims, loudness.
---

# Motion director film

Design, animate, score and QA a finished film in code. A film with no bugs is not finished; it is finished when it holds up next to the best work in its genre and any references in the brief. Everything below is the floor, not the ceiling.

**Precedence**: the brief wins, then any kit or repo the brief names, then these defaults.

## Start with the brief

1. Copy [references/brief-template.md](references/brief-template.md) into `brief.md` in a fresh working folder (never inside this skill).
2. Fill what the user gave you. For every blank line, decide it yourself and write the choice with a one-line reason. Use the defaults table in the template.
3. Read `autonomy`. **Gated**: stop at every ◆ in the workflow and show the user the artefact. **Unattended**: never stop; record each ◆ decision in `ledger.md` and keep going.

## Pick the mode

- **showreel**: the craft is the subject. Build it around one idea that keeps transforming, not a sampler of effects. Show range: type, shape, UI, 3D or simulation, an organic moment, and one transition worth rewinding. A new composition every 1–2.5 s, with one or two held breaths. No fake clients, logos or metrics.
- **product**: the product is the hero. Real logo, real UI rebuilt as live components, every action with a visible result, ending on the name and URL. A new composition every 1.4–3.5 s.
- **launch-story**: characters carry the release. Write 2–3 treatments and pick one. Characters act: readable poses, holds on faces, funny timing. One or two facts at most, woven into the world.
- **explainer**: one cause and effect. Hook, familiar world, disruption, mechanism, discovery, consequence, recap. Narration at 125–145 wpm, and on-screen labels never repeat the narration.

## Workflow

1. **Lock facts.** Write `facts.json`: every claim that may appear on screen or in voice, its exact source sentence and its URL. The `facts` line of the brief is the only source. Collect the real assets (see Assets).
2. **Study.** Go through the references (see Assets for how). For public work, also look at how this audience talks about the subject now.
3. **Concept.** Write 2–3 directions and pick one. Name three signature moments without using effect names ("the cursor becomes the logo", not "a morph").
4. **Storyboard.** A table with columns: time, on screen, purpose, audio cue, exit, and what carries over to the next shot. It must read with the sound off. Run a critic on it. ◆
5. **Style bible.** At most 6 colours, local fonts, textures and a motion vocabulary (eases, durations, how things enter and leave). Render three style frames in code, plus character sheets and key poses if the mode needs them. ◆
6. **Audio and timing map.** Build the audio first (see Audio), write `timing.json`, and play the audio-only mix. ◆
7. **Build, assemble, critique.** Build the scenes (see Build), assemble the full film, and run the critic loop until the quality bar passes.
8. **Deliver** the full set (see Deliverables). ◆ If asked, save the pipeline as a reusable skill.

## Assets

- Capture the real product at 2×. Take the logo as SVG from the source, and sample the real colours and fonts. Never redraw a logo.
- Never show a raw screenshot as a static slab. Rebuild its panels, icons and text as live HTML/SVG so each part can move.
- Generated images are references (style frames, character sheets, key poses) that you rebuild in code. They go on screen only if the brief allows it, and then labelled as concept.
- References are for study. Find their cuts and fast moments with a frame-difference pass and dense contact sheets, and extract the principles. Never copy footage, layouts or music.

## Craft rules

1. Frame one is a finished picture that works as a still on a busy feed. The hook lands in the first second.
2. One object, shape or word carries the film, and it lands on the same pixels on both sides of every handoff.
3. Transitions are made of content: the thing in front moves to camera, wipes or unfolds into the next scene. Hard cuts only when size, direction and subject match, and only on a beat.
4. One lead movement with overlapping secondary ones. Nothing starts or stops all at once.
5. Speed always changes: arrive slowly enough to read, leave fast. No linear easing. Use anticipation, follow-through, squash and stretch, springs and arcs.
6. Every action has a visible result.
7. Type is motion, not captions: it enters, masks and reveals. Keep it on screen about 0.3 s per word, 0.7 s minimum, and never over busy picture without a plate behind it. If the picture says it, cut the word.
8. Vary scale and layout: macro, wide, overhead, full-frame type. The subject fills the frame. Never repeat a layout.
9. Holds breathe with micro-motion; nothing freezes. Camera moves are motivated, with motion blur on the fast ones.
10. 3D only where it explains something spatial. Product-shoot lighting, a camera at 35–55°, real materials, and labels as HTML tracked from the 3D scene.
11. Every effect earns its place. No decorative particles, generic gradients or stock glitches.

## Audio

Audio comes first, and the picture is cut to it. Skip this section only when `sound: silent`, and still write `timing.json` from a tempo you choose.

- Music matches the energy and sits low. Never name a brand or artist in a music-generation prompt. Trim or offset a track rather than bend the picture to fit it.
- Detect beats and write `timing.json`: beats, the drop, voice in/out frames, and key actions snapped to beats. All animation timing reads from this file; never hard-code a hit time in a scene.
- Sound effects only for real on-screen events: one soft whoosh per scene change, and clicks and impacts on real actions, each in its own frequency range just above the music.
- Voices: audition two per character and two takes per line. Mouths follow loudness and stay still in silence. Duck the music under dialogue.
- Mix to about −14 LUFS integrated with true peak ≤ −1 dBTP. Export a music-only version as well.

## Build

- Everything is code on one timeline, with pinned local fonts and assets, rendered frame by frame and encoded with ffmpeg. API keys stay in environment variables, never in files.
- Before real work, render a 3–5 s test end to end (scene → frames → audio → MP4) to prove the pipeline.
- Every value is a function of the frame number. No timers, no wall clock, no unseeded randomness. Rendering the same frame twice gives identical pixels.
- Write shared tokens, eases and handoff positions first, then build each scene as its own component. Scene builders can run in parallel because the handoffs are fixed up front.
- Recompose each aspect ratio rather than cropping, and keep 9:16 content out of the platform UI zones (top bar, right-hand action rail, bottom caption area).
- Toolchain default when the brief leaves it blank: Remotion for React/UI products; otherwise a headless-browser frame renderer driving an HTML + GSAP timeline seeked to each frame.

## Critic loop

The builder never judges its own work. After the storyboard, after each scene and after every full render, a fresh critic subagent that has seen none of the building pulls its own frames (every 0.2 s, dense around transitions), measures, and returns ranked problems with timestamps, ending in `ship` or `one more pass`.

Every full render also gets a sound-off read (story retold from a silent 2 fps contact sheet), a sync check (every hit and line within 1 frame of `timing.json`), a fact check (every word traced to `facts.json`) and a director's review (a blunt critique of what feels assembled, slow or generic).

Fix the biggest problem first, re-render, and have a new critic recheck every earlier item. Log each round in `ledger.md` with before and after numbers. Sampling, the ledger format and measurement commands are in [references/critic-loop.md](references/critic-loop.md).

## Quality bar

Ship only when all of these pass. Record each with its measured value.

- Exact duration, size and frame rate.
- Frame one is finished.
- At most 1 s frozen per 30 s, and no still stretch over 0.5 s.
- Text contrast ≥ 4.5:1, no collisions, inside safe margins.
- Brand colours match in the encoded render.
- Cuts and hits within 1 frame of the beat.
- Loudness about −14 LUFS, no clipping, effects below music and voice.
- Understood with the sound off.
- Every claim is in `facts.json`, and nothing is invented: no testimonials, ratings, prices, results or real people. Anything generated is labelled.
- Judged: a critic would put it beside the references without it looking weaker.

## Guardrails

- Never put a claim on screen or in voice that is not in `facts.json`.
- Never redraw a logo, never invent clients, metrics or quotes, never copy reference footage, layouts or music.
- Never let the builder sign off its own render.
- Keep working files, renders, captured assets and keys out of this skill folder.

## Deliverables

- The final MP4 for each format, and a music-only version.
- A 10–20 frame contact sheet.
- `brief.md`, `facts.json`, the style bible, `timing.json`, `ledger.md`.
- The quality-bar results with measured values.
- A short note on what a human should still check by eye and ear.

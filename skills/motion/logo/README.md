# Logo Skills

Skills for animating logos and other line-drawn marks: taking a flat piece of artwork apart into pieces that can move, and landing them back on the artwork exactly.

<!-- skills:start -->
| Skill | Use it for |
| --- | --- |
| [Logo Mask Motion](logo-mask-motion/SKILL.md) | Move the pieces of a line-drawn mark with masks and land on the artwork |
<!-- skills:end -->

## Use a skill

Copy the complete skill folder into your agent's skills directory, or run `python3 install.py` from the repo root for Claude Code. Then describe the motion you want and give the agent the artwork:

```text
Use $logo-mask-motion to make the petals of this outlined logo fan out from a closed bud and land exactly on the artwork, with masks.
```

In Claude Code you can also just describe it ("animate the pieces of this logo sliding out from behind each other") or type `/logo-mask-motion`.

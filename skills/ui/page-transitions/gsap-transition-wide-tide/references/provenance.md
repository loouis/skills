# Reference and validation record

Captured 2026-09-27 from the owner's original private motion study and current navigation integration. This public package includes only the six reusable curve definitions, motion mechanics and generic integration examples. Client artwork, fonts, copy and private source locations are omitted.

- Frozen archive SHA-256: `b3f981c169a30934685f183d95caa1a791f36fcda08a34578eebdff074ef97b1`.
- Original shape/timing module SHA-256: `87a88504b39e9841e77d81e107e45b412d25258fd65baac7508f4aca93c146f8`.
- Original three-front portrait module SHA-256: `c25ecb5c57a95515dcfebb93b34fdc9c838559856ca1059cd2e7e1059c0c8e58`.

The archive and all 20 members matched their manifest before extraction. The six bundled shape definitions match the corresponding source objects exactly. A direct parity comparison of all six pure renderers at 1/600-second intervals from 0–2.25s passed (8,106 poses). No private archive is required to use these skills.

The first three rounded mobile fronts preserve the reference constants. Adaptive viewport mapping and the covered loader pattern follow the current site integration. Double Swell, Signature Loop and Figure Eight portrait cover widths are new extensions in this package. Lifecycle code is a reusable rewrite with isolated sessions, signal handling and cleanup; it is not asserted byte-identical to the router-specific source.

Run `node --test scripts/*.test.mjs` inside a skill directory. These tests cover six curves, handoff/endpoint geometry, nine viewport sizes, linear clock sequencing, delayed readiness, superseded navigation, abort/failure cleanup, reduced motion and bounded readiness. Browser checks verified all six variants at frames 59–61: both desktop and portrait panel interiors have identical solid-color pixels across the handoff. Geometry checks cover the edge/corner regions independently. Browser controls verified slow-load hold, cancellation and reduced-motion bypass. An isolated two-route Astro 7.3.5 app passed type checks and production build; forward/back navigation completed with an idle overlay, two retained paths and no console errors. The standalone bundle matches the module renderer. Demo previews are browser captures normalized to the repository’s 1280 × 720 export size. Physical-device validation is still recommended in the receiving site; numerical coverage is not a claim of physical-device testing.

For maintainers with the original shape module available, run `node --experimental-strip-types scripts/check-reference.mjs <original-shape-module.ts>` to repeat parity checks. Keep private locations out of repository files and command transcripts committed here.

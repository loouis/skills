# Reference comparison, boxes and scoring

First state the requested optical effect and identify comparable features: transparent centre, bright/dark contour, broad folded faces, air/water orientation, curved product contact, first reflected letter and calm open-water region. Do not infer a reference's authoring method, camera or wetting physics from appearance alone.

1. Retain each real render in a fresh revision with source/settings, same-run raw/denoised images and hashes. Keep the actual reference outside the public skill.
2. Compare whole-frame composition first, then matching native regions. Use separate vector/HTML boxes for the contact and near lettering, plus another region for open water. A box is a review overlay; never bake it into the beauty pixels. Provide a clean/annotated toggle and label the defect or observed improvement.
3. Inspect raw and denoised output side by side. Retain the original reference framing; don't imply pixel alignment for different cameras. A small crop enlarged on screen does not establish native detail.
4. Score five fixed criteria, out of10, with one concrete observation each. Mean them equally. Record what still differs and the single next change most likely to help. Do not raise a score just because checks pass, resolution rises or a requested threshold remains unmet.
5. Retain regressions. If later feedback reveals a missed defect, withdraw the old readiness claim while preserving the historical score and evidence. Stop when the requested scope is honestly satisfied; explain a concrete limit when it is not.

## Rubrics

For an isolated optical specimen: clear transmission; controlled contours/highlights; broad-to-fine shape hierarchy; reference-feature compatibility; native cleanliness.

For product-water contact: curved front contact and rising sides; natural local ripples; reflection warp close to the waterline; calm surroundings with sustained lower distortion; whole-shot water integration.

The selected contact still's ratings were[9.0,8.8,9.1,9.1,9.0],mean9.0. These are reviewer assessments of that still. User feedback subsequently accepted the ripple/water direction; it did not assign the numeric score or approve motion. Historical isolated drop/cavity/fold scores of9 likewise do not become scores for the public demos or future applications.

For a whole product shot, also review composition, product/print fidelity, material readability, water integration and final cleanliness. Report the weaker of the whole-shot and water assessments as overall readiness so strong typography cannot hide weak water.

## Score recorder

`scripts/score_pass.py` accepts five supplied ratings, hashes existing evidence and refuses an existing output. It does not inspect pixels or invent a score. `--specimen contact` selects the contact rubric; the other options select the optical rubric.

```sh
python3 scripts/score_pass.py --pass-id A01 --specimen contact \
  --image /tmp/study/beauty.png --raw /tmp/study/raw.png \
  --reference /tmp/reference.jpg --criteria 8.8 8.4 9 9 8.8 \
  --defects 'Local ripple spacing remains regular.' \
  --comparison 'Front join curves downward; first reflected bend is still late.' \
  --next-change 'Vary local phase gently while preserving the far pool.' \
  --output /tmp/study/A01-score.json
```

Passing topology, preservation, replay or hash checks earns no visual points. Keep those facts alongside, rather than inside, the beauty score.

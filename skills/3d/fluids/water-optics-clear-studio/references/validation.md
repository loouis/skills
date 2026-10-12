# Validation and limits

Package checked on13October2026 with Blender5.2.1 LTS, CPU Cycles.

- The public droplet, cavity and fold examples were freshly generated at640×640,256 samples maximum,45 seconds per-image sampling cap. Saved scenes reopened before rendering; closed-mesh topology, cavity orientation, exact configuration, device, dimensions, sample limit and IOR checks passed. Same-render raw and denoised PNGs were retained locally and converted to same-size JPEGs for the demo.
- Native beauty/raw views were inspected. They show clear centres, differentiated water/air boundaries and the broad-to-fine folded surface. The fold retains grain and denoising softness. These portable demo renders have no9/10 production claim.
- The detached contact formula was compared against the selected source at401×507 coordinates, five times and both full/quiet branches:2,033,070 scalar height values, maximum absolute difference0m. This checks extraction parity, not a new product render or motion quality.
- Six numerical tests cover downward-front contact direction, finite heights/far water, agreement of plate fields near contact, local temporal continuity, smooth contribution gain and removal of the fine repeated ripple. Run `scripts/test_field.py` using Python with NumPy, or Blender's Python. It does not require a source-project scene.

The source contact study retained18 drafts and two full-resolution stills, then selected the narrower curved rim and small ripple treatment. The final water-interaction self-score was9.0/10; later user feedback was positive about the ripple/water appearance. No full film was created by that contact refinement. Historical scenes, source references and client product assets are not distributed here.

The source optical study's component scores were9/10 after iterative review. Those historical scores are scoped subjective assessments; they do not transfer to this public CPU demo, new products, resolutions, backends or animation. Public geometry is procedural, with no branded artwork or reference imagery. Physical wetting, equilibrium shape, buoyancy, coupled fluid dynamics and loops remain outside the demonstrated result.

The public demo was checked at desktop and mobile widths: all images loaded, the raw/denoised and annotation toggles worked, there was no horizontal overflow, and no console warning/error was reported. Repository validation passes for20 skills in6 categories; skill metadata, relative references, Python syntax and public-content checks pass.

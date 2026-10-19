# Selected recipe: useful values, explicit limits

These are reproducibility notes for a studied Blender 5.2.1 LTS scene, not a turnkey preset or measured physical specification. Values depend on source assets, node graphs, UV scale, scene scale, light distance/size and colour pipeline. Build a new scene with the workflow, then tune against references. Do not copy numbers in isolation and claim a match.

## Selected lineage

Fuller fringe/sofa/stool baseline R110 → kitchen R112 → R113 → R114 → R115 → R119 → wall-light R120 → material/light R121 → R122 → R123 → R124 → R125 → continuous-rug R127. R123's stone is restored in R124. R126's four-tile rug is rejected and is not a dependency. R128 is a rejected material-only control. R111 and R116–R118 are unselected diagnostic branches.

A new project need not replay these scripts or numbers. Preserve the same dependency discipline: accepted textile and furniture state survives kitchen work; rejected experiments never silently enter the selected build.

## Materials

| Surface | Selected art-direction values |
| --- | --- |
| Travertine009 | Physical source repeat 1.2×1.2 m; HSV value 1.08, saturation .38; roughness remap .205–.315; normal strength .13; bump strength .17; IOR 1.52 |
| White oak veneer | HSV value 1.33, saturation .67; beige mix .10; roughness .29–.43; coat .10, coat roughness .30; member-aligned UVs retained |
| Champagne bronze | Linear shader RGB (.57,.43,.26), metallic 1, roughness .195, anisotropic .22; reflected scene retained |
| Tan nubuck | Restrained RGB ramp (.151,.084,.044) to (.170,.099,.052); broad noise 27; sheen .34, sheen roughness .62, specular IOR level .26; bump distance .00018 m at .38 strength, secondary .000075 m |
| Oiled floor / smoked oak table | Roughness .30–.47, individually aligned grain |
| Fine rug | Approximately 6 mm yarn pitch, reduced relief, short fibres ≤.65 mm rise; sheen .62, diffuse roughness .65, specular level .18; noise scale 6000, bump .00007 m at .45 strength, subtle colour multiplier .88–1.10 |
| Rug backing | Normal .65, bump .0008 m plus secondary .0002 m, sheen .5; retained footprint and support crown |

Node noise scales depend on coordinates. These values are incomplete without the coordinate mapping; they are starting comparisons, not physically meaningful weave pitch by themselves. Source map roles and GL normal convention must remain correct. The natural slab species/finish is not certified by a texture name.

Selected source assets: Poly Haven white_oak_veneer, oak_wood_planks, rough_linen, knitted_fleece and qwantani_morning_puresky; ambientCG Travertine009. Retain current source licences and authors. The public package ships none of these image maps.

## Light balance

- Sun energy 8; direction vector approximately (-.68,1,-.24), angular size .035 radians; colour (1,.93,.81).
- Broad exterior sky area source 360 W, colour (.86,.93,1).
- HDR world strength .24, exposure +.65 stops.
- Kitchen LED 6.5 W, appliance photographic fill .5 W, seating return 18 W.
- Seating return excluded from glossy/transmission rays; area-source transmission exclusions documented separately.

Direction needs the receiving scene's axis convention. Source dimensions/positions and the original HDR orientation are not encoded by this table; therefore these values alone cannot reconstruct the light field. Keep the declared photographic aids separate from site/sun claims. Use matched controls to tune new architecture.

## Geometry and soft detail

Island 3200×1050×900 mm finished; top and ends 70 mm; 400 mm recess. Two-column/three-row drawer bank with 3 mm reveals and real underside pull lips. Low selected stool reference 550×550×850 mm, seat 630 mm; custom estimated reconstruction, not manufacturer CAD.

Sofa lift 40 mm on six short supports; seat crown about 455 mm. Cloth supported zones follow sofa; free drape receives continuous shaping. Waffle repeat 7.5 mm, relief up to 1.4 mm, separate warp/weft and short fibres. Fuller fringe: four header courses, 369 groups of 18–22 yarns, 7,415 continuous paths, 59,320 loose ends, nominal 9 mm woven lead-ins. These are dense case geometry, not minimum counts.

Rug: one continuous field, 620 rows×1181 steps×5 sides (3,661,100 vertices), 28,000 short fibres. Continuous grid removes tile seams; footprint/backing/support crown unchanged. Use a lighter implementation if final viewing scale permits; verify equivalence visually.

Curtain relaxation was artist deformation up to 11.91 mm with fixed top anchors and unchanged horizontal envelope. Accepted cloth derives from a stable gravity envelope plus explicit artist corrections, not the rejected rest-shape simulation experiments.

## Production evidence

The selected scene packed 30 file images, passed 168 saved-scene screens and 6 nominal planning checks, and was inspected through 26 delivered views, 7 contact sheets, 13 individual critical images, 9 annotated boards and 5 comparisons. Critical renders used 2240×1260/256 samples; secondary 1600×900/128. These counts describe the scope of that review, not requirements or proof of quality.

Keep a separate record for technical checks and appearance. Open limitations included uniform veneer, strong pale highlights, tailored furniture refinement and repeat rhythms in textile detail. A temporary AI coast plate was explicitly illustrative; true site/floor outlook, product-specific installation and construction compliance remained unresolved.

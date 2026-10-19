# Materials, mapping and asset integrity

## Scale and finish hierarchy

Use scene metres and document physical texture scale. Establish colour management before tuning surfaces. Stone, wood, metal, glass, plaster and fabric must return light differently. Similar colours can remain distinct through roughness, depth, relief and reflection structure.

| Material | Desired response | Common failure |
| --- | --- | --- |
| Honed ivory stone | Broad soft highlights, fine pores/bands, quiet mineral variation | Flat beige, wet mirror finish, crater pores or blotchy large noise |
| Pale oak joinery | Directional grain, modest panel variation, broad satin sheen | Orange wash, one continuous texture through all doors, grain across members |
| Oiled floor/smoked table | Readable grain, quieter reflections than hardware | Mirror floor, identical boards, wrong edge orientation |
| Champagne metal | Related bright/dark reflected bands on curved form | Yellow diffuse object, pure white outline or featureless black metal |
| Upholstery/nubuck | Soft grazing sheen, small-scale yarn/nap, broad calm variation | Plastic sheen, sandy bump, cloudy mottling |
| Wall/plaster | Quiet colour and broad gradients | Sandpaper noise or dirt added to manufacture detail |
| Clear glass | Transmission plus angle-dependent reflections, real edges | Invisible sheet, grey opaque plate or reflection plane pasted over view |

## Reliable texture loading

Choose exact files and declared map roles. A broad `*rough*` search once connected `rough_linen_diff` to roughness because the asset name contained “rough”. Check the actual upstream image node and colour space, not merely the shader input label.

- Base-colour/diffuse maps: colour-managed sRGB unless the asset specifies otherwise.
- Roughness, normal, height and other numeric data: Non-Color.
- Match the normal convention; use the supplied OpenGL normal for Blender or convert deliberately. Do not mix DX/GL silently.
- Check bit depth, alpha use, displacement units, UV scale and map alignment.
- Roughness range remapping is a look-development choice; retain source maps and licence even when the finish is custom.
- Do not call a procedurally authored material a photographic scan. The selected ambientCG Travertine009 was procedural.

## UV workflow

Create panel/member mapping that follows construction. Tall joinery generally has deliberate vertical grain; rails, legs, edge bands and tabletop faces need their own direction. View all exposed faces after every transform. Rotate by member orientation, not world height. Use limited per-panel offsets/variation rather than stretching one patch across the whole wall.

For stone, plan slab cuts and material scale before Boolean sink openings. Maintain an unfolded edge treatment so veins meet intentionally through a waterfall corner. Recheck the active render UV map after modifier/Boolean operations. Triplanar mapping can be useful for an early blockout but does not solve manufactured grain direction.

For fabric, use surface UVs carried through the drape. Place warp/weft in textile coordinates, then evaluate the deformed surface. Pattern should bend with folds rather than remain projected in world space. Inspect stretching at pinch zones and unequal folds.

## Reflection diagnosis order

Before editing a glossy material, isolate:

1. Geometry and silhouette: is there a ridge, gap or faceting?
2. Normals/tangents: is the shading smooth and consistent with intended bevels?
3. Material response: correct metalness, IOR, roughness, normal scale?
4. Reflected environment: bright wall, ceiling, source or missing off-camera architecture?
5. Sampling/denoising: has the highlight been smeared or broken?

Keep camera/exposure unchanged in diagnostic comparisons. A reflection can look like a bulge without any mesh deformation. A pale hob can be correctly reflecting a ceiling. Avoid painting over either in a clean direct-render workflow.

## Packing and portability

Record source page, licence, author when given, downloaded filename, map role, physical scale and hash in the receiving project. Separate source geometry from custom finishes. Poly Haven/ambientCG resources in the studied recipe were CC0; manufacturer furniture and product photographs were not. Recheck rights when sourcing anew.

Pack expected file textures before delivery and reopen the saved blend to verify nonempty packed bytes. Do not filter packing solely through `image.has_data`: lazy-loaded images may lack evaluated pixels but still be required. Check UDIMs, sequences, linked libraries, caches and fonts separately; not every dependency becomes portable merely because image packing succeeds. Keep a dependency manifest and resolve missing files before calling the scene self-contained.

Preservation signatures should include evaluated geometry where appropriate, transforms, modifiers, active UVs, material assignments/node values, visibility and cameras. A vertex-position hash alone does not capture a changed shader, flipped UV or disabled modifier. Define intended changes narrowly and audit exceptions independently.

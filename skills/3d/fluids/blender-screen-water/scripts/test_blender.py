"""Check configured FLIP scene and water nodes without baking or rendering."""
import json
import math
from pathlib import Path
import sys
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'assets/recipe'))
import bpy
from build_fall import bake
from water_helpers import material,panel,render_setup

with tempfile.TemporaryDirectory(prefix='screen-water-blender-') as temp:
    output=Path(temp)/'simulation'
    domain,inlet,lip=bake(output,prepare_only=True)
    d=domain.modifiers[0].domain_settings
    assert d.resolution_max==256 and d.mesh_scale==2 and d.cache_type=='ALL'
    assert d.cache_mesh_format=='BOBJECT' and d.cache_data_format=='UNI'
    assert abs(d.flip_ratio-.94)<1e-6 and abs(d.time_scale-.5)<1e-6
    assert d.timesteps_min==2 and d.timesteps_max==6
    assert d.use_collision_border_front is False and d.use_collision_border_top is False
    assert all(abs(a-b)<1e-5 for a,b in zip(domain.dimensions,(.60,2.12,.40)))
    assert all(abs(a-b)<1e-5 for a,b in zip(inlet.dimensions,(.565,.075,.13)))
    assert inlet.hide_render and lip.hide_render
    for frame in [1,31,91,178]:
        bpy.context.scene.frame_set(frame)
        v=inlet.modifiers[0].flow_settings.velocity_coord
        expected=(.10*math.sin(frame*.095),-.48-.11*math.sin(frame*.073),.12+.035*math.sin(frame*.067))
        assert all(abs(a-b)<1e-6 for a,b in zip(v,expected)),(frame,list(v),expected)
    bpy.ops.wm.open_mainfile(filepath=str(output/'waterfall.blend'))
    domain=bpy.data.objects['Liquid | descending water-wall domain']
    assert Path(bpy.path.abspath(domain.modifiers[0].domain_settings.cache_directory)).resolve()==(output/'cache').resolve()
    assert json.loads((output/'settings.json').read_text())['baked'] is False
    assert not list((output/'cache').rglob('*.bobj.gz'))
    card=panel('Test card',(-.7,.2,1.25),(.60,3),9)
    assert not card.visible_camera and not card.visible_shadow
    assert card.visible_glossy and card.visible_transmission
    assert len(card.data.uv_layers)==1
    nodes=card.data.materials[0].node_tree.nodes
    assert len([n for n in nodes if n.type=='MATH' and n.operation=='COSINE'])==2
    scene=bpy.context.scene;render_setup(scene)
    assert scene.cycles.device=='CPU' and scene.cycles.samples==128
    assert scene.render.resolution_x==480 and scene.render.resolution_y==1800
    assert scene.render.image_settings.color_depth=='8' and scene.render.fps==30
    assert scene.cycles.transmission_bounces==8 and scene.cycles.seed==29
    try: bake(output,prepare_only=True)
    except FileExistsError: pass
    else: raise AssertionError('Existing simulation was not protected')
print('ok: configured FLIP settings, inlet keyframes, save/reopen, cards, render setup and overwrite guard')

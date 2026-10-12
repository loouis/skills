"""Meaningful small native fixture tests; no production-motion or beauty claim."""
import copy
import json
from pathlib import Path
import sys
import tempfile

import bpy
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
from splash_tools import configure, freeze, fresh_output, recipe, refine, weights

base=Path(tempfile.mkdtemp(prefix='splash-native-test-'))
checks={}
fresh_output(base/'protected')
try:fresh_output(base/'protected')
except FileExistsError:checks['refuses_existing_output']=True
cfg=recipe()
field=cfg['filter']['field']
w=weights([[0,0,.17],[.3,0,.17],[0,0,.05],[0,0,.30]],field)
checks['bounded_field']=np.allclose(w,[1,0,0,0])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,radius=.025,location=(0,0,.17))
obj=bpy.context.object
before=np.array([v.co[:] for v in obj.data.vertices])
filter_cfg=copy.deepcopy(cfg['filter'])
filter_cfg.update(base_factor=0,base_iterations=1,factor=0,iterations=1,subdivision=0)
refine(obj,filter_cfg)
after=np.array([v.co[:] for v in obj.data.vertices])
distance=np.linalg.norm(after-before,axis=1)
checks['bounded_offset']=bool(np.all(distance<=.001801) and np.max(distance)>.00179)
checks['vertex_group_cleanup']=len(obj.vertex_groups)==0
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_cube_add(size=.075,location=(0,-.015,.17))
bpy.context.object['splash_source']=True
bpy.context.object['splash_role']='sheet'
cfg['domain'].update(resolution=24,mesh_scale=1,frames=[1,3],timesteps=[1,2])
out=fresh_output(base/'bake')
result=configure(out,cfg)
domain=bpy.data.objects[result['domain']]
checks['source_role_velocity']=all(tuple(o.modifiers['Splash initial volume'].flow_settings.velocity_coord)==tuple(np.array(cfg['source']['velocity']['sheet'],np.float32)) for o in bpy.context.scene.objects if o.get('splash_source'))
try:freeze(domain.name,2)
except ValueError:checks['rejects_unbaked_freeze']=True
bpy.ops.wm.save_as_mainfile(filepath=str(out/'simulation.blend'))
bpy.ops.object.select_all(action='DESELECT')
domain.select_set(True)
bpy.context.view_layer.objects.active=domain
bpy.ops.fluid.bake_all()
bpy.ops.wm.save_as_mainfile(filepath=str(out/'simulation.blend'))
bpy.ops.wm.open_mainfile(filepath=str(out/'simulation.blend'))
frozen=freeze(result['domain'],2)
checks['resolved_frozen_geometry']=len(frozen.data.vertices)>24
checks['cache_independent_frozen_mesh']=not any(m.type=='FLUID' for o in bpy.context.scene.objects for m in o.modifiers)
vertices=len(frozen.data.vertices)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'frozen.blend'))
bpy.ops.wm.open_mainfile(filepath=str(out/'frozen.blend'))
checks['frozen_reopens']=len(bpy.data.objects['Frozen splash'].data.vertices)==vertices
frozen=bpy.data.objects['Frozen splash']
before=np.array([v.co[:] for v in frozen.data.vertices])
result=refine(frozen,recipe()['filter'])
after=np.array([v.co[:] for v in frozen.data.vertices])
checks['default_filter_changes_shape']=bool(np.max(np.abs(after-before))>1e-6)
checks['default_filter_preserves_topology']=len(after)==vertices
checks['subdivision_restored']=len(frozen.modifiers)==1 and frozen.modifiers[0].type=='SUBSURF'
assert len(checks)==12 and all(checks.values()),checks
(base/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print('NATIVE_TESTS',str(base),json.dumps(checks),flush=True)

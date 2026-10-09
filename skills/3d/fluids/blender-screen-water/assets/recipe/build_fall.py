"""Prepare or bake a generic top-fed Mantaflow water sheet in a new directory."""
import argparse, json, math, sys, time
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from water_helpers import cube
from recipe_io import fresh_output, recipe_hashes

def bake(output, prepare_only=False):
 path=fresh_output(output)
 path.mkdir(parents=True,exist_ok=False)
 (path/'cache').mkdir()
 bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.frame_start=1;s.frame_end=180;s.render.fps=30;s.render.threads_mode='FIXED';s.render.threads=8
 # The screen is viewed along Z. Gravity has a downward Y component and a
 # smaller component against the back surface: an inclined water-wall study.
 s.gravity=(0,-3.8,-2.0)
 domain=cube('Liquid | descending water-wall domain',(0,0,.14),(.60,2.12,.40))
 mod=domain.modifiers.new('Mantaflow','FLUID');mod.fluid_type='DOMAIN';d=mod.domain_settings;d.domain_type='LIQUID'
 d.resolution_max=256;d.cache_type='ALL';d.cache_directory=str(path/'cache');d.cache_frame_start=1;d.cache_frame_end=180
 d.cache_mesh_format='BOBJECT';d.cache_data_format='UNI';d.use_mesh=True;d.mesh_scale=2;d.mesh_particle_radius=1.45;d.mesh_smoothen_pos=1;d.mesh_smoothen_neg=1;d.mesh_generator='IMPROVED';d.flip_ratio=.94;d.particle_randomness=.08
 d.time_scale=.50;d.timesteps_min=2;d.timesteps_max=6;d.cfl_condition=2;d.use_diffusion=True;d.viscosity_base=1;d.viscosity_exponent=6;d.surface_tension=.3
 d.use_collision_border_front=False;d.use_collision_border_top=False
 inlet=cube('Supply | broad top inlet',(0,1.005,.055),(.565,.075,.13))
 fm=inlet.modifiers.new('Continuous water supply','FLUID');fm.fluid_type='FLOW';f=fm.flow_settings;f.flow_type='LIQUID';f.flow_behavior='INFLOW';f.use_initial_velocity=True;f.surface_distance=1.5;inlet.hide_render=True;inlet.display_type='WIRE'
 # Small changing crossflow creates irregular folds without reversing descent.
 for frame in range(1,181,3):
  f.velocity_coord=(.10*math.sin(frame*.095),-.48-.11*math.sin(frame*.073),.12+.035*math.sin(frame*.067));f.keyframe_insert(data_path='velocity_coord',frame=frame)
 # Rounded submerged lip gives the incoming water a visible roll at the top.
 bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=.07,depth=.66,location=(0,.91,-.035),rotation=(0,math.pi/2,0))
 lip=bpy.context.object;lip.name='Supply | rounded submerged lip';bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 lm=lip.modifiers.new('Physical lip','FLUID');lm.fluid_type='EFFECTOR';lm.effector_settings.effector_type='COLLISION';lip.hide_render=True;lip.display_type='WIRE'
 bpy.ops.object.select_all(action='DESELECT');domain.select_set(True);bpy.context.view_layer.objects.active=domain
 settings={'frames':180,'fps':30,'gravity':list(s.gravity),'time_scale':.5,'resolution':256,'mesh_scale':2,'domain_center':[0,0,.14],'domain_scale':2.12,'recipe_hashes':recipe_hashes(),'blender_version':bpy.app.version_string,'baked':False}
 (path/'settings.json').write_text(json.dumps(settings,indent=2)+'\n')
 bpy.ops.wm.save_as_mainfile(filepath=str(path/'waterfall.blend'))
 if not prepare_only:
  started=time.monotonic()
  bpy.ops.fluid.bake_all()
  settings['baked']=True
  settings['bake_seconds']=time.monotonic()-started
  (path/'settings.json').write_text(json.dumps(settings,indent=2)+'\n')
  bpy.ops.wm.save_as_mainfile(filepath=str(path/'waterfall.blend'))
 return domain,inlet,lip

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--output',type=Path,required=True)
 p.add_argument('--prepare-only',action='store_true',help='Save the configured scene without baking')
 args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
 bake(args.output,args.prepare_only)

if __name__=='__main__': main()

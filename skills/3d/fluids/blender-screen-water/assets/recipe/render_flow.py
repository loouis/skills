"""Render cold or hot bubbles inside cached descending FLIP water."""
import argparse, json, math, random, sys, time
from pathlib import Path
import bpy
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from water_helpers import cube,material,panel,render_setup
from recipe_io import render_output, read_bobj, parse_frames

def render(simulation, output, mode, frames, scale=1, samples=128, device='CPU'):
 if mode not in ('cold','hot'): raise ValueError('Mode must be cold or hot')
 if not isinstance(scale,int) or not 1<=scale<=4 or samples<1: raise ValueError('Use scale 1–4 and positive samples')
 frames=list(frames)
 if not frames or any(not isinstance(f,int) or not 1<=f<=180 for f in frames): raise ValueError('Frames must be in 1–180')
 sim=Path(simulation).expanduser().resolve()
 settings={'mode':mode,'width':480*scale,'height':1800*scale,'samples':samples,'device':device,'bubble_seeds':9000 if mode=='hot' else 3000,'fps':30,'frames':[1,180],'blender_version':bpy.app.version_string}
 path=render_output(output,sim,frames,settings)
 bpy.ops.wm.read_factory_settings(use_empty=True)
 s=bpy.context.scene
 hot=mode=='hot'
 base=cube('Screen | deep charcoal backing',(0,0,-.063),(.70,2.20,.015));bm,bp=material('Charcoal',(.0015,.002,.0025),1);bp.inputs['Specular IOR Level'].default_value=0;base.data.materials.append(bm)
 s.world=bpy.data.worlds.new('Black studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.18,.20,.23,1);s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.10
 panel('Silver reflection | left',(-.7,.2,1.25),(.60,3),9);panel('Silver reflection | right',(.8,-.3,1),(.30,2.2),11);panel('Soft fill',(0,.4,2.8),(3,4),.45)
 bpy.ops.object.camera_add(location=(0,0,4));cam=bpy.context.object;cam.name='Camera | screen only';cam.data.type='ORTHO';cam.data.ortho_scale=1.80;cam.rotation_euler=(0,0,0);s.camera=cam
 m,p=material('Clear water | IOR 1.333',(.985,.995,1),.008);p.inputs['IOR'].default_value=1.333;p.inputs['Transmission Weight'].default_value=1
 n=m.node_tree.nodes;l=m.node_tree.links;tc=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.noise_dimensions='4D';noise.inputs['Scale'].default_value=110;noise.inputs['Detail'].default_value=2.5;noise.inputs['Roughness'].default_value=.6;l.new(tc.outputs['Object'],noise.inputs['Vector']);b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.20;b.inputs['Distance'].default_value=.0008;l.new(noise.outputs['Fac'],b.inputs['Height']);l.new(b.outputs['Normal'],p.inputs['Normal'])
 # Real 3D air inclusions, placed against each physical liquid surface.
 # Their clustering/advection is art-directed; the primary water remains FLIP.
 air,ap=material('Entrained air | water-to-air interface',(1,1,1),.035);ap.inputs['IOR'].default_value=1/1.333;ap.inputs['Transmission Weight'].default_value=1
 rng=random.Random(82);seeds=[]
 for k in range(9000 if hot else 3000):
  group=k%3;center=[-.175,.14,-.035][group]
  seeds.append((center+rng.gauss(0,.063 if hot else .048),rng.random(),.0014+rng.random()**2*.0060,rng.random()*6.283,rng.random()))
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1);template=bpy.context.object;tv=[tuple(v.co) for v in template.data.vertices];tf=[tuple(f.vertices) for f in template.data.polygons];bpy.data.objects.remove(template,do_unlink=True)
 bubbles=None
 render_setup(s,w=480*scale,h=1800*scale,samples=samples,device=device);water=None
 for frame in frames:
  target=path/f'water-{frame:04d}.png'
  if target.exists():continue
  vertices,faces=read_bobj(sim/'cache/mesh'/f'fluid_mesh_{frame:04d}.bobj.gz')
  if water:old=water.data;bpy.data.objects.remove(water,do_unlink=True);bpy.data.meshes.remove(old)
  me=bpy.data.meshes.new('Physical flowing surface');me.from_pydata(vertices,[],faces);me.update();water=bpy.data.objects.new('Water | top-fed physical FLIP mesh',me);s.collection.objects.link(water);water.location=(0,0,.14);water.scale=(2.12,)*3;water.data.materials.append(m)
  for poly in me.polygons:poly.use_smooth=True
  if bubbles:old=bubbles.data;bpy.data.objects.remove(bubbles,do_unlink=True);bpy.data.meshes.remove(old)
  tree=BVHTree.FromPolygons([(x*2.12,y*2.12,z*2.12+.14) for x,y,z in vertices],faces,all_triangles=True)
  bv=[];bf=[];t=(frame-1)/30
  for x0,phase,rad,angle,variation in seeds:
   age=(t*.5+phase*1.17)%1.17
   y=(-1.03+.70*age+1.55*age*age) if hot else (1.01-.48*age-1.90*age*age)
   if y<-.96 or y>.94:continue
   # Uneven moving pockets leave areas of clear glass between dense clusters.
   birth=t*.5-age
   if math.sin(birth*9+phase*2+angle*.15)<(-.72 if hot else -.42):continue
   x=x0+.015*math.sin(age*8+angle)+.02*math.sin(birth*4)
   if abs(x)>.27:continue
   hit,normal,idx,distance=tree.ray_cast((x,y,.40),(0,0,-1),.6)
   if hit is None or hit.z<-.048:continue
   z=hit.z-rad*.8;index=len(bv);sx=1+.14*math.sin(angle+age*3);sy=1.0+.20*variation
   bv.extend([(x+vx*rad*sx,y+vy*rad*sy,z+vz*rad*.86) for vx,vy,vz in tv]);bf.extend([tuple(index+v for v in face) for face in tf])
  bme=bpy.data.meshes.new('Air pockets | clustered advected geometry');bme.from_pydata(bv,[],bf);bme.update();bubbles=bpy.data.objects.new('Water | entrained bubbles',bme);s.collection.objects.link(bubbles);bubbles.data.materials.append(air)
  for poly in bme.polygons:poly.use_smooth=True
  noise.inputs['W'].default_value=frame/30*.18;s.frame_set(frame);s.render.filepath=str(path/f'water-{frame:04d}.partial.png');t=time.monotonic();bpy.ops.render.render(write_still=True);Path(s.render.filepath).replace(target);print('FRAME_DONE',frame,round(time.monotonic()-t,2),flush=True)
  if frame==90:bpy.ops.wm.save_as_mainfile(filepath=str(path/'waterfall-look.blend'))


def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--simulation',type=Path,required=True)
 p.add_argument('--output',type=Path,required=True)
 p.add_argument('--mode',choices=['cold','hot'],required=True)
 p.add_argument('--frames',default='1:181',help='Comma-separated frames or exclusive-end ranges')
 p.add_argument('--scale',type=int,default=1)
 p.add_argument('--samples',type=int,default=128)
 p.add_argument('--device',choices=['CPU','METAL','CUDA','OPTIX','HIP','ONEAPI'],default='CPU')
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
 render(a.simulation,a.output,a.mode,parse_frames(a.frames),a.scale,a.samples,a.device)

if __name__=='__main__': main()

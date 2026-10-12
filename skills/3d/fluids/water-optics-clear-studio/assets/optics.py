"""Procedural optical benches: no scene, brand, font, or external texture inputs.
Geometry dimensions are Blender units; setup assigns the specimen unit scale.
Backend is explicitly CPU. Render jobs are created by scripts/render_demo.py.
"""
import bpy, bmesh, numpy as np, math, json
from mathutils import Vector

def look(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()

def mesh(name,v,f,mat,smooth=True):
 m=bpy.data.meshes.new(name);m.from_pydata(v.tolist() if hasattr(v,'tolist') else v,[],f);m.update()
 o=bpy.data.objects.new(name,m);bpy.context.scene.collection.objects.link(o);m.materials.append(mat)
 for p in m.polygons:p.use_smooth=smooth
 return o

def water(rough):
 m=bpy.data.materials.new('Water | neutral dielectric, IOR 1.333');m.use_nodes=True;n=m.node_tree.nodes;n.clear()
 g=n.new('ShaderNodeBsdfGlass');g.distribution='BECKMANN';g.inputs['Color'].default_value=(1,1,1,1);g.inputs['Roughness'].default_value=rough;g.inputs['IOR'].default_value=1.333
 out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(g.outputs[0],out.inputs['Surface']);return m

def emit(name,col,power):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(*col,1);e.inputs[1].default_value=power
 out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],out.inputs['Surface']);return m

def plane(name,loc,scale,mat,target=(0,0,0)):
 bpy.ops.mesh.primitive_plane_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.scale=(*scale,1);look(o,target);o.data.materials.append(mat);return o

def card(name,loc,scale,power,soft=False):
 m=emit(name,(1,1,1),power);n=m.node_tree.nodes;l=m.node_tree.links
 tc=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['UV'],sep.inputs[0]);es=[]
 for axis in ['X','Y']:
  sub=n.new('ShaderNodeMath');sub.operation='SUBTRACT';sub.inputs[1].default_value=.5;l.new(sep.outputs[axis],sub.inputs[0])
  ab=n.new('ShaderNodeMath');ab.operation='ABSOLUTE';l.new(sub.outputs[0],ab.inputs[0])
  mr=n.new('ShaderNodeMapRange');mr.clamp=True;mr.interpolation_type='SMOOTHSTEP';mr.inputs['From Min'].default_value=0 if soft else .37;mr.inputs['From Max'].default_value=.5;mr.inputs['To Min'].default_value=power;mr.inputs['To Max'].default_value=0;l.new(ab.outputs[0],mr.inputs[0]);es.append(mr)
 mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';l.new(es[0].outputs[0],mul.inputs[0]);l.new(es[1].outputs[0],mul.inputs[1]);l.new(mul.outputs[0],next(x for x in n if x.type=='EMISSION').inputs[1])
 o=plane(name,loc,scale,m);o.visible_camera=False;return o

def background(cfg,grid):
 m=emit('Refracted cool-white background',(.8,.9,1),1);n=m.node_tree.nodes;l=m.node_tree.links
 tc=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=2.8;noise.inputs['Detail'].default_value=1.0;l.new(tc.outputs['Generated'],noise.inputs['Vector'])
 ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.15;ramp.color_ramp.elements[0].color=(cfg['bg']*(1-cfg['blue']),cfg['bg']*(1-cfg['blue']*.4),cfg['bg'],1)
 ramp.color_ramp.elements[1].position=.85;ramp.color_ramp.elements[1].color=(cfg['bg']*1.12,cfg['bg']*1.12,cfg['bg']*1.12,1);l.new(noise.outputs['Fac'],ramp.inputs[0]);col=ramp.outputs['Color']
 if cfg.get('bluefield') and not grid:
  geo=n.new('ShaderNodeNewGeometry');dist=n.new('ShaderNodeVectorMath');dist.operation='DISTANCE';l.new(geo.outputs['Position'],dist.inputs[0]);dist.inputs[1].default_value=(.065,-.035,-.13)
  mr=n.new('ShaderNodeMapRange');mr.clamp=True;mr.interpolation_type='SMOOTHSTEP';mr.inputs['From Min'].default_value=.005;mr.inputs['From Max'].default_value=.115;mr.inputs['To Min'].default_value=.90;mr.inputs['To Max'].default_value=0;l.new(dist.outputs['Value'],mr.inputs[0]);mix=n.new('ShaderNodeMixRGB');l.new(mr.outputs[0],mix.inputs[0]);l.new(col,mix.inputs[1]);mix.inputs[2].default_value=(.07,.30,.68,1);col=mix.outputs[0]
 if grid:
  sep=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['Object'],sep.inputs[0]);lines=[]
  for a in ['X','Y']:
   mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=math.pi/.006;l.new(sep.outputs[a],mul.inputs[0])
   sin=n.new('ShaderNodeMath');sin.operation='SINE';l.new(mul.outputs[0],sin.inputs[0]);ab=n.new('ShaderNodeMath');ab.operation='ABSOLUTE';l.new(sin.outputs[0],ab.inputs[0])
   lt=n.new('ShaderNodeMath');lt.operation='LESS_THAN';lt.inputs[1].default_value=.085;l.new(ab.outputs[0],lt.inputs[0]);lines.append(lt)
  mx=n.new('ShaderNodeMath');mx.operation='MAXIMUM';l.new(lines[0].outputs[0],mx.inputs[0]);l.new(lines[1].outputs[0],mx.inputs[1]);mix=n.new('ShaderNodeMixRGB');l.new(mx.outputs[0],mix.inputs[0]);l.new(col,mix.inputs[1]);mix.inputs[2].default_value=(.05,.08,.12,1);col=mix.outputs[0]
 l.new(col,next(x for x in n if x.type=='EMISSION').inputs[0]);o=plane('Background | behind all water boundaries',(0,0,-.13),(1,1),m,target=(0,0,1))
 # Keep Object coordinates in metres for the diagnostic grid.
 bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 return o

def receiver(s,variant,cfg):
 m=bpy.data.materials.new('Diffuse caustic receiver');m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*cfg.get('floorcolor',(.48,.66,.82)),1);p.inputs['Roughness'].default_value=1
 o=plane('Physical receiver beneath water',(0,0,cfg.get('floordepth',-.058)),(.8,.8),m,target=(0,0,1));o.cycles.is_caustics_receiver=True
 if cfg.get('receiverup'):o.rotation_euler=(0,0,0)
 light=bpy.data.lights.new('Small caustic source','AREA');light.energy=cfg.get('lightpower',8);light.shape='DISK';light.size=cfg.get('lightsize',.012);light.cycles.is_caustics_light=variant!='no-caustics'
 ob=bpy.data.objects.new(light.name,light);s.collection.objects.link(ob);ob.location=(-.09,.10,.40);look(ob,(0,0,0))
 for o in s.objects:
  if o.type=='MESH' and any(m and m.name.startswith('Water |') for m in o.data.materials):o.cycles.is_caustics_caster=True

def ball(mat,invert=False,cfg=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=192,ring_count=128,radius=.016,location=(0,0,0));o=bpy.context.object;o.name='Air cavity | normals point water into air' if invert else 'Water droplet | normals point water into air'
 for v in o.data.vertices:
  x,y,z=v.co/.016;fac=1+.035*x*y+.022*math.sin(3*y+2*x)*(1-z*z)
  v.co=(x*.016*fac,y*.016*.96*fac,z*.016*.93*fac)
  if invert and cfg.get('oblate'):
   v.co.x*=1+.08*math.sin(3*y+.5);v.co.y*=.87;v.co.z*=.38
   if cfg.get('pocketcurl'):v.co.z+=.0018*(1-x*x-y*y)*math.exp(-((x-.25)**2+(y+.1)**2)/.35)
 if invert:
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 for p in o.data.polygons:p.use_smooth=True
 o.data.materials.append(mat);return o

def height(x,y,cfg,flat=False):
 if flat:return np.full_like(x,.020)
 z=.009*np.sin(39*x+16*y)+.007*np.cos(34*y-17*x+.8)
 z+=.014*np.exp(-((x+.020+.016*np.sin(43*y))/.018)**2)
 z+=.007*np.exp(-((y-.023-.018*np.sin(45*x+.5))/.012)**2)
 if cfg.get('steep'):
  z+=.025*np.exp(-((x+.020+.026*np.sin(44*y))/.009)**2)
  z+=.019*np.exp(-((y-.020-.020*np.sin(53*x+.5))/.010)**2)
 # Spatially localized capillary packets, not blanket noise or a bump map.
 for cx,cy,wl,amp,width in [(-.022,-.027,.0040,.00028,.037),(.032,.018,.0032,.00018,.027)]:
  rr=np.sqrt((x-cx)**2+(y-cy)**2+.0000001)
  if cfg.get('warp'):rr+=.002*np.sin(80*x+20*y)+.0013*np.cos(47*y-10*x)
  if not cfg.get('mixed'):z+=cfg['ripple']*amp*np.sin(2*math.pi*rr/wl+.5*np.sin(50*x))*np.exp(-(rr/width)**2)
 if cfg.get('mixed'):
  for i in range(11):
   theta=i*2.399963;wl=.0045+.008*(.5+.5*math.sin(i*2.3));phase=(x*math.cos(theta)+y*math.sin(theta)+.002*np.sin(x*35+y*27+i))*2*math.pi/wl+i
   amp=.00010*(.5+.5*math.cos(i*1.8));envelope=np.exp(-((x-.012)**2+(y+.018)**2)/.075**2)
   z+=cfg['ripple']*amp*np.sin(phase)*envelope
 return .020+cfg['fold']*z

def body(mat,cfg,fold=False,flat=False,density=501):
 N=density if fold else 2;extent=.15
 if not fold and cfg.get('immersed'):extent=5
 xx,yy=np.meshgrid(np.linspace(-extent,extent,N),np.linspace(-extent,extent,N));zz=height(xx,yy,cfg,flat) if fold else np.full_like(xx,5 if cfg.get('immersed') else .04)
 vv=np.c_[xx.ravel(),yy.ravel(),zz.ravel()];f=[]
 for j in range(N-1):
  for i in range(N-1):q=j*N+i;f.append((q,q+1,q+N+1,q+N))
 edge=list(range(N))+[j*N+N-1 for j in range(1,N)]+[(N-1)*N+i for i in range(N-2,-1,-1)]+[j*N for j in range(N-2,0,-1)]
 off=len(vv);low=vv[edge].copy();low[:,2]=-5 if not fold and cfg.get('immersed') else -.045;vv=np.concatenate([vv,low]);ne=len(edge)
 for i in range(ne):f.append((edge[(i+1)%ne],edge[i],off+i,off+(i+1)%ne))
 f.append(tuple(range(off+ne-1,off-1,-1)));o=mesh('Closed folded water volume' if fold else 'Closed surrounding water',vv,f,mat)
 # Front-only smooth normals; planar rear/sides remain planar.
 for p in o.data.polygons[(N-1)**2:]:p.use_smooth=False
 return o

def studio(w,cfg):
 n=w.node_tree.nodes;l=w.node_tree.links;n.clear();tc=n.new('ShaderNodeTexCoord');direction=tc.outputs['Normal']
 def calc(op,*vals):
  a=n.new('ShaderNodeMath');a.operation=op
  for i,v in enumerate(vals):
   if isinstance(v,(float,int)):a.inputs[i].default_value=v
   else:l.new(v,a.inputs[i])
  return a.outputs[0]
 field=None
 for d,width,power in [((-.5,.6,.6),.24,7),((.8,.2,.1),.16,4),((-.2,-.7,.5),.40,1.2)]:
  dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';l.new(direction,dot.inputs[0]);dot.inputs[1].default_value=Vector(d).normalized()
  f=calc('MULTIPLY',power,calc('EXPONENT',calc('MULTIPLY',-1/width**2,calc('SUBTRACT',1,dot.outputs['Value']))));field=f if field is None else calc('ADD',field,f)
 field=calc('ADD',cfg['world'],field);bg=n.new('ShaderNodeBackground');bg.inputs[0].default_value=(.82,.92,1,1);l.new(field,bg.inputs[1]);out=n.new('ShaderNodeOutputWorld');l.new(bg.outputs[0],out.inputs[0])

def setup(cfg,size,samples,spec,variant):
 cfg=dict(cfg)
 if variant=='grid-sphere':cfg['oblate']=False;cfg['pocketcurl']=False
 bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.unit_settings.system='METRIC'
 s.render.engine='CYCLES';s.cycles.samples=samples;s.cycles.use_denoising=False;s.cycles.adaptive_threshold=.012;s.cycles.adaptive_min_samples=32
 s.cycles.max_bounces=16;s.cycles.transmission_bounces=16;s.cycles.glossy_bounces=8;s.cycles.diffuse_bounces=4;s.cycles.sample_clamp_direct=0;s.cycles.sample_clamp_indirect=0
 if variant.startswith('b'):s.cycles.max_bounces=s.cycles.transmission_bounces=int(variant[1:])
 s.cycles.caustics_reflective=True;s.cycles.caustics_refractive=True;s.cycles.seed=41
 s.cycles.device='CPU'
 s.render.resolution_x=size;s.render.resolution_y=size;s.render.resolution_percentage=100
 s.cycles.time_limit=0
 s.cycles.transparent_max_bounces=8;s.cycles.volume_bounces=0;s.cycles.blur_glossy=1.0
 s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.color_depth='16'
 s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=0
 if spec=='fold':s.view_settings.exposure=cfg.get('exposure',0);s.view_settings.look=cfg.get('look','AgX - Medium High Contrast')
 s.render.film_transparent=False;s.render.image_settings.compression=35;s.cycles.pixel_filter_type='BLACKMAN_HARRIS';s.cycles.filter_width=1.0
 w=bpy.data.worlds.new('Neutral studio world');s.world=w;w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(.82,.9,1,1);w.node_tree.nodes['Background'].inputs[1].default_value=cfg['world']
 if cfg.get('studio') and not (spec=='fold' and cfg.get('darkfold')):studio(w,cfg)
 bpy.ops.object.camera_add(location=(0,0,.55));cam=bpy.context.object;cam.name='Optical bench camera';look(cam,(0,0,0));cam.data.type='ORTHO';cam.data.ortho_scale=.065 if spec!='fold' else .145;cam.data.lens=100;cam.data.dof.use_dof=False;s.camera=cam
 if spec=='fold' and cfg.get('tilt'):cam.location=(0,-cfg.get('angle',.28),.24);look(cam,(0,0,.02))
 background(cfg,variant.startswith('grid'))
 if variant!='no-cards' and not cfg.get('studio'):
  card('Large left softbox',(-.13,.065,.18),(.10,.27),cfg['key'])
  card('Right slim softbox',(.16,.02,.10),(.034,.20),cfg['fill'])
  card('Upper softbox',(.015,.20,.12),(.24,.04),1.4)
 if variant!='no-cards' and cfg.get('softcards') and (not (spec=='fold' and cfg.get('darkfold')) or cfg.get('foldcards')):
  card('Feathered left reflection',(-.12,.11,.16),(.10,.17),cfg.get('foldkey',cfg['key']) if spec=='fold' else cfg['key'],True)
  card('Feathered right reflection',(.16,-.02,.08),(.035,.18),cfg.get('foldfill',cfg['fill']) if spec=='fold' else cfg['fill'],True)
 if spec=='fold' and cfg.get('strip') and variant!='no-cards':card('Fine white reflection field',(0,.20,.24),(.28,.035),cfg.get('strippower',7),True)
 if spec!='fold' and cfg.get('glint'):
  light=bpy.data.lights.new('Small photographic glint','AREA');light.energy=cfg.get('glintpower',.08);light.shape='DISK';light.size=.008
  ob=bpy.data.objects.new(light.name,light);s.collection.objects.link(ob);ob.location=cfg.get('glintpos',(-.10,.15,.20));look(ob,(0,0,0))
 black=emit('Black flags',(.004,.005,.008),1)
 for side in ([-1,1] if cfg['flag'] else []):
  o=plane('Dark side flag', (side*.20,-.015,.015),(cfg['flag'],.5),black);o.visible_camera=False
 if cfg.get('rearflags') and spec!='fold':
  # Classic bright-field photography: dark material beyond the frame is
  # refracted into a contour. Nothing is painted onto the water surface.
  flags=emit('Rear flag optical grey',(.8,.9,1),cfg.get('flagpower',.004))
  for side in [-1,1]:
   x=side*cfg.get('flagx',.09);plane('Rear dark field flag', (x,0,-.065),(.10,.30),flags,target=(x,0,1))
 mat=water(cfg['rough'])
 if spec=='droplet':ball(mat,cfg=cfg)
 elif spec=='cavity':body(mat,cfg);ball(mat,invert=True,cfg=cfg)
 elif spec=='fold':body(mat,cfg,True,variant=='flat',density=cfg.get('density',701 if size>=1400 else 401))
 else:raise ValueError(spec)
 if spec=='fold' and cfg.get('receiver') and variant!='grid':receiver(s,variant,cfg)
 if spec=='fold' and cfg.get('removeback') and variant!='grid':bpy.data.objects['Background | behind all water boundaries'].hide_render=True
 if variant=='caustics-only':
  w.node_tree.nodes['Background'].inputs[1].default_value=0
  for o in s.objects:
   if o.name.startswith(('Feathered','Fine white','Background |')):o.hide_render=True
 if cfg.get('physicalscale') and spec!='fold':
  scale=.1 if spec=='droplet' else .3
  for o in s.objects:o.location*=scale;o.scale*=scale
  cam.data.ortho_scale*=scale
 if cfg.get('physicalunits') and spec!='fold':s.unit_settings.scale_length=.1 if spec=='droplet' else .3
 s.cycles.adaptive_threshold=.004 if cfg.get('denoise') else .012
 if cfg.get('denoise'):
  s.cycles.use_denoising=True;s.view_layers[0].cycles.denoising_store_passes=True
 s['optics_effective_config']=json.dumps(cfg)
 return s

def raw_output(s,out,key):
 nt=bpy.data.node_groups.new('Raw and denoised optical evidence','CompositorNodeTree');s.compositing_node_group=nt
 nt.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');rl=nt.nodes.new('CompositorNodeRLayers');go=nt.nodes.new('NodeGroupOutput');nt.links.new(rl.outputs['Image'],go.inputs['Image'])
 fo=nt.nodes.new('CompositorNodeOutputFile');fo.directory=str(out);fo.file_name=key+'-raw-';fo.format.media_type='IMAGE';fo.format.file_format='PNG';fo.format.color_mode='RGB';fo.format.color_depth='16';fo.save_as_render=True
 fo.file_output_items.clear();fo.file_output_items.new('RGBA','Image');nt.links.new(rl.outputs['Noisy Image'],fo.inputs[0])

def audit(s):
 rec={}
 for o in s.objects:
  if o.type=='MESH' and any(m and m.name.startswith('Water |') for m in o.data.materials):
   bm=bmesh.new();bm.from_mesh(o.data);rec[o.name]={'vertices':len(bm.verts),'faces':len(bm.faces),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume':bm.calc_volume(signed=True)};bm.free()
 return rec

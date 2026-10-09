"""Generic geometry, reflection cards and water render settings."""
import bpy, math
from mathutils import Vector

def cube(name, loc, dim):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o=bpy.context.object; o.name=name; o.dimensions=dim
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return o

def material(name, color, roughness):
    m=bpy.data.materials.new(name);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=roughness
    return m,p

def look(o,target):
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()

def panel(name,loc,size,strength):
    bpy.ops.mesh.primitive_plane_add(size=1,location=loc)
    o=bpy.context.object;o.name=name;look(o,(0,0,.10));o.scale=(*size,1)
    o.visible_camera=False;o.visible_shadow=False
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;n.clear()
    out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');em.inputs['Color'].default_value=(.94,.97,1,1)
    uv=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(uv.outputs['UV'],sep.inputs[0])
    vals=[]
    for axis in ['X','Y']:
        sub=n.new('ShaderNodeMath');sub.operation='SUBTRACT';sub.inputs[1].default_value=.5;l.new(sep.outputs[axis],sub.inputs[0])
        mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=math.pi*2;l.new(sub.outputs[0],mul.inputs[0])
        co=n.new('ShaderNodeMath');co.operation='COSINE';l.new(mul.outputs[0],co.inputs[0])
        add=n.new('ShaderNodeMath');add.operation='MULTIPLY_ADD';add.inputs[1].default_value=.5;add.inputs[2].default_value=.5;l.new(co.outputs[0],add.inputs[0]);vals.append(add)
    prod=n.new('ShaderNodeMath');prod.operation='MULTIPLY';l.new(vals[0].outputs[0],prod.inputs[0]);l.new(vals[1].outputs[0],prod.inputs[1])
    gain=n.new('ShaderNodeMath');gain.operation='MULTIPLY';gain.inputs[1].default_value=strength;l.new(prod.outputs[0],gain.inputs[0]);l.new(gain.outputs[0],em.inputs['Strength']);l.new(em.outputs[0],out.inputs['Surface']);o.data.materials.append(m)
    return o

def render_setup(s,w=480,h=1800,samples=128,device="CPU"):
    s.render.engine='CYCLES';s.cycles.samples=samples;s.cycles.use_denoising=True
    s.cycles.adaptive_threshold=.015;s.cycles.adaptive_min_samples=24
    s.cycles.max_bounces=10;s.cycles.transmission_bounces=8;s.cycles.glossy_bounces=6
    s.cycles.caustics_reflective=False;s.cycles.caustics_refractive=False
    s.cycles.sample_clamp_indirect=3
    s.cycles.seed=29;s.cycles.use_animated_seed=False
    s.render.resolution_x=w;s.render.resolution_y=h;s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.color_depth='8'
    s.render.fps=30;s.render.use_persistent_data=True
    s.render.threads_mode='FIXED';s.render.threads=8
    if device == 'CPU':
        s.cycles.device='CPU'
    else:
        p=bpy.context.preferences.addons['cycles'].preferences
        p.compute_device_type=device
        if device == 'METAL':
            p.kernel_optimization_level='OFF'
        p.get_devices()
        found=False
        for d in p.devices:
            d.use=d.type==device
            found=found or d.use
        if not found:
            raise RuntimeError('Requested Cycles device unavailable: '+device)
        s.cycles.device='GPU'
    s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=0

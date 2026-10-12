"""Render an original optical fixture, not a fluid bake or production splash."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import bpy
import numpy as np
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from splash_tools import fresh_output, water_material


def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()


def emission(name, colour, strength):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    light = nodes.new('ShaderNodeEmission')
    light.inputs[0].default_value = (*colour, 1)
    light.inputs[1].default_value = strength
    out = nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(light.outputs[0], out.inputs[0])
    return mat


def card(name, location, scale, strength):
    bpy.ops.mesh.primitive_plane_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = (*scale, 1)
    aim(obj, (0, 0, .15))
    obj.visible_camera = False
    mat = emission(name, (1, 1, 1), strength)
    obj.data.materials.append(mat)
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    tc, sep = nodes.new('ShaderNodeTexCoord'), nodes.new('ShaderNodeSeparateXYZ')
    links.new(tc.outputs['UV'], sep.inputs[0])
    fields = []
    for axis in ['X', 'Y']:
        sub, ab = nodes.new('ShaderNodeMath'), nodes.new('ShaderNodeMath')
        sub.operation, ab.operation = 'SUBTRACT', 'ABSOLUTE'
        sub.inputs[1].default_value = .5
        links.new(sep.outputs[axis], sub.inputs[0])
        links.new(sub.outputs[0], ab.inputs[0])
        ramp = nodes.new('ShaderNodeMapRange')
        ramp.clamp, ramp.interpolation_type = True, 'SMOOTHERSTEP'
        for key, value in [('From Min', .04), ('From Max', .5), ('To Min', 1), ('To Max', 0)]:
            ramp.inputs[key].default_value = value
        links.new(ab.outputs[0], ramp.inputs[0])
        fields.append(ramp.outputs[0])
    multiply = nodes.new('ShaderNodeMath')
    multiply.operation = 'MULTIPLY'
    links.new(fields[0], multiply.inputs[0])
    links.new(fields[1], multiply.inputs[1])
    mix, transparent = nodes.new('ShaderNodeMixShader'), nodes.new('ShaderNodeBsdfTransparent')
    links.new(multiply.outputs[0], mix.inputs[0])
    links.new(transparent.outputs[0], mix.inputs[1])
    links.new(next(n for n in nodes if n.type == 'EMISSION').outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], next(n for n in nodes if n.type == 'OUTPUT_MATERIAL').inputs[0])


def point(u, v):
    return (.20 * u, -.065 + .037 * u*u + .022 * math.sin(v*5 + .6*math.sin(u*3)),
            .145 + .052*v + .012*math.sin(u*4 + v) - .012*u*u)


def curve(name, points, radius, material):
    data = bpy.data.curves.new(name, 'CURVE')
    data.dimensions = '3D'
    data.resolution_u = 1
    data.bevel_depth, data.bevel_resolution = radius, 4
    data.use_fill_caps = True
    spline = data.splines.new('POLY')
    spline.points.add(len(points)-1)
    for p, xyz in zip(spline.points, points):
        p.co = (*xyz, 1)
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    data.materials.append(material)
    return obj


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.render.threads_mode, scene.render.threads = 'FIXED', 8
    scene.cycles.samples, scene.cycles.time_limit = 256, 60
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = 'OPENIMAGEDENOISE'
    scene.cycles.adaptive_threshold = .006
    scene.view_layers[0].cycles.denoising_store_passes = True
    scene.cycles.max_bounces = scene.cycles.transmission_bounces = 16
    scene.cycles.transparent_max_bounces = 12
    scene.render.resolution_x, scene.render.resolution_y = 768, 480
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format, scene.render.image_settings.color_mode = 'PNG', 'RGB'
    scene.render.image_settings.color_depth = '16'
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - Medium High Contrast'
    scene.unit_settings.system = 'METRIC'
    scene.world = bpy.data.worlds.new('Quiet studio')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs[0].default_value = (.009,.017,.04,1)
    scene.world.node_tree.nodes['Background'].inputs[1].default_value = .15
    water = water_material()
    nu, nv = 200, 90
    vertices = [point(u,v) for u in np.linspace(-1,1,nu+1) for v in np.linspace(-1,1,nv+1)]
    holes = [(-.76,.40,.115,.25),(.73,-.28,.11,.22),(.92,.57,.16,.29)]
    faces = []
    for i in range(nu):
        for j in range(nv):
            u, v = -1+(i+.5)*2/nu, -1+(j+.5)*2/nv
            if any(((u-x)/rx)**2+((v-y)/ry)**2 < 1 for x,y,rx,ry in holes):
                continue
            k = i*(nv+1)+j
            faces.append((k,k+nv+1,k+nv+2,k+1))
    data = bpy.data.meshes.new('Generic folded membrane')
    data.from_pydata(vertices, [], faces)
    data.update()
    obj = bpy.data.objects.new('Generic folded membrane', data)
    scene.collection.objects.link(obj)
    data.materials.append(water)
    for polygon in data.polygons:
        polygon.use_smooth = True
    smooth = obj.modifiers.new('Round sampled margins','SUBSURF')
    smooth.levels = smooth.render_levels = 1
    shell = obj.modifiers.new('Closed water thickness','SOLIDIFY')
    shell.thickness, shell.offset, shell.use_even_offset = .0022, 0, False
    for sign in [-1,1]:
        pts=[point(u,sign) for u in np.linspace(-1,1,220)]
        curve('Accumulated edge',pts,.0017,water)
    for x,y,rx,ry in holes[:2]:
        pts=[point(x+rx*math.cos(a),y+ry*math.sin(a)) for a in np.linspace(0,2*math.pi,180)]
        curve('Rounded hole rim',pts,.0015,water)
    rng=np.random.default_rng(407)
    for k in range(28):
        side = -1 if k%2 else 1
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,radius=rng.uniform(.0008,.0025),
            location=(side*rng.uniform(.198,.234),rng.uniform(-.08,-.035),rng.uniform(.085,.217)))
        drop=bpy.context.object
        drop.name='Detached droplet'
        drop.scale.z=rng.uniform(.9,1.45)
        drop.data.materials.append(water)
        for polygon in drop.data.polygons:polygon.use_smooth=True
    bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=.034,depth=.255,location=(.012,.028,.137))
    product=bpy.context.object
    product.name='Generic coral cylinder'
    product.rotation_euler.y=.10
    bevel=product.modifiers.new('Rounded ends','BEVEL')
    bevel.width,bevel.segments=.012,6
    mat=bpy.data.materials.new('Coral ceramic')
    mat.use_nodes=True
    p=mat.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(.54,.037,.014,1)
    p.inputs['Roughness'].default_value=.22
    product.data.materials.append(mat)
    for polygon in product.data.polygons:polygon.use_smooth=True
    bpy.ops.mesh.primitive_plane_add(size=2,location=(0,.55,.15))
    back=bpy.context.object
    back.name='Blue backdrop'
    aim(back,(0,-1,.15))
    back.data.materials.append(emission('Cobalt field',(.006,.044,.17),1))
    card('Broad left',(-.35,-.22,.40),(.4,.45),14)
    card('Right diffusion',(.36,-.02,.25),(.23,.42),11)
    card('Rear low',(0,.20,-.26),(.7,.4),20)
    card('Top',(0,.15,.5),(.6,.22),16)
    bpy.ops.object.camera_add(location=(.04,-1.8,.48))
    camera=bpy.context.object
    camera.data.type='ORTHO'
    camera.data.ortho_scale=.53
    camera.data.clip_start=.001
    aim(camera,(0,0,.15))
    scene.camera=camera
    scene['fixture_scope']='Original authored optical fixture, not a native fluid simulation'
    return scene


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    output=fresh_output(args.output)
    scene=build()
    tree=bpy.data.node_groups.new('Same-run raw','CompositorNodeTree')
    scene.compositing_node_group=tree
    tree.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
    layers=tree.nodes.new('CompositorNodeRLayers')
    final=tree.nodes.new('NodeGroupOutput')
    tree.links.new(layers.outputs['Image'],final.inputs['Image'])
    raw=tree.nodes.new('CompositorNodeOutputFile')
    raw.directory,raw.file_name=str(output),'raw-'
    raw.format.media_type='IMAGE'
    raw.format.file_format,raw.format.color_mode,raw.format.color_depth='PNG','RGB','16'
    raw.save_as_render=True
    raw.file_output_items.clear()
    raw.file_output_items.new('RGBA','Image')
    tree.links.new(layers.outputs['Noisy Image'],raw.inputs[0])
    scene.render.filepath=str(output/'beauty.png')
    bpy.ops.wm.save_as_mainfile(filepath=str(output/'scene.blend'),compress=True)
    bpy.ops.render.render(write_still=True)
    bpy.ops.wm.open_mainfile(filepath=str(output/'scene.blend'))
    scene=bpy.context.scene
    glass=next(n for n in bpy.data.materials['Neutral water in air'].node_tree.nodes if n.type=='BSDF_GLASS')
    checks={'size':(scene.render.resolution_x,scene.render.resolution_y)==(768,480),
        'ior':abs(glass.inputs['IOR'].default_value-1.333)<1e-6,
        'neutral':tuple(glass.inputs['Color'].default_value)==(1,1,1,1),
        'roughness':glass.inputs['Roughness'].default_value==0,
        'closed_shell':scene.objects['Generic folded membrane'].modifiers.get('Closed water thickness') is not None,
        'no_fluid_claim':not any(m.type=='FLUID' for o in scene.objects for m in o.modifiers),
        'raw_pair':(output/'raw-Image.png').exists()}
    assert all(checks.values()),checks
    record={'blender':bpy.app.version_string,'checks':checks,'scope':scene['fixture_scope'],
        'hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in output.glob('*.png')}}
    (output/'verification.json').write_text(json.dumps(record,indent=2)+'\n')
    print('DEMO_VERIFIED',json.dumps(checks),flush=True)


if __name__=='__main__':main()

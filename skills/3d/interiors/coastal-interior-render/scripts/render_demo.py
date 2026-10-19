"""Create an original, asset-free material vignette; not a furnished apartment."""
import argparse
import json
import math
import sys
from pathlib import Path
import bpy
from mathutils import Vector


def material(name, colour, rough=.5, metal=0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*colour, 1)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    return m, p


def noise_finish(mat, colour_a, colour_b, mapping_scale, bump_distance, rough_a, rough_b):
    n, l = mat.node_tree.nodes, mat.node_tree.links
    p = n.get('Principled BSDF')
    tex = n.new('ShaderNodeTexCoord')
    mapping = n.new('ShaderNodeVectorMath'); mapping.operation = 'MULTIPLY'
    mapping.inputs[1].default_value = mapping_scale
    l.new(tex.outputs['Object'], mapping.inputs[0])
    noise = n.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 1
    noise.inputs['Detail'].default_value = 3
    l.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    ramp = n.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (*colour_a, 1)
    ramp.color_ramp.elements[1].color = (*colour_b, 1)
    l.new(noise.outputs['Fac'], ramp.inputs[0]); l.new(ramp.outputs['Color'], p.inputs['Base Color'])
    rough = n.new('ShaderNodeMapRange')
    rough.inputs['To Min'].default_value = rough_a; rough.inputs['To Max'].default_value = rough_b
    l.new(noise.outputs['Fac'], rough.inputs['Value']); l.new(rough.outputs[0], p.inputs['Roughness'])
    bump = n.new('ShaderNodeBump'); bump.inputs['Distance'].default_value = bump_distance
    bump.inputs['Strength'].default_value = .2
    l.new(noise.outputs['Fac'], bump.inputs['Height']); l.new(bump.outputs[0], p.inputs['Normal'])


def box(name, location, dimensions, mat, bevel=.002):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    o = bpy.context.object; o.name = name; o.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    if bevel:
        mod = o.modifiers.new('Small eased edges', 'BEVEL'); mod.width = bevel; mod.segments = 3
        o.modifiers.new('Corner normals', 'WEIGHTED_NORMAL')
    return o


def tube(name, points, radius, mat):
    data = bpy.data.curves.new(name, 'CURVE'); data.dimensions = '3D'
    data.bevel_depth = radius; data.bevel_resolution = 5
    spline = data.splines.new('POLY'); spline.points.add(len(points)-1)
    for p, xyz in zip(spline.points, points): p.co = (*xyz, 1)
    o = bpy.data.objects.new(name, data); bpy.context.collection.objects.link(o)
    data.materials.append(mat)
    return o


def point_at(obj, target):
    obj.rotation_euler = (Vector(target)-obj.location).to_track_quat('-Z', 'Y').to_euler()


def area(name, position, target, energy, size, colour):
    data = bpy.data.lights.new(name, 'AREA'); data.energy = energy; data.shape = 'DISK'; data.size = size
    data.color = colour
    obj = bpy.data.objects.new(name, data); bpy.context.collection.objects.link(obj)
    obj.location = position; point_at(obj, target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    output = args.output.expanduser().resolve()
    if output.exists(): raise FileExistsError('Choose a fresh output directory')
    output.mkdir(parents=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene; sc.unit_settings.system = 'METRIC'; sc.unit_settings.scale_length = 1
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 64
    sc.cycles.use_denoising = True
    sc.view_settings.view_transform = 'AgX'; sc.view_settings.exposure = 0
    sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.render.resolution_percentage = 100
    plaster, _ = material('Warm mineral wall', (.53,.49,.42), .8)
    stone, _ = material('Quiet procedural stone', (.65,.59,.47), .28)
    noise_finish(stone, (.49,.435,.35), (.72,.665,.55), (4,4,18), .0002, .24,.34)
    oak, p = material('Procedural vertical oak study', (.36,.23,.12), .35)
    p.inputs['Coat Weight'].default_value = .1
    noise_finish(oak, (.23,.15,.085), (.47,.34,.20), (65,65,1.8), .00012,.29,.43)
    bronze, p = material('Muted bronze reflection study', (.57,.43,.26), .195, 1)
    p.inputs['Anisotropic'].default_value = .22
    cloth, p = material('Flax surface sample', (.54,.48,.38), .74)
    p.inputs['Sheen Weight'].default_value = .45
    noise_finish(cloth, (.44,.395,.32), (.61,.56,.47), (750,750,750), .00015,.65,.8)
    dark, _ = material('Recess shadow material', (.07,.055,.04), .65)
    floor, _ = material('Pale floor', (.43,.40,.34), .55)
    box('Floor', (0,0,-.05), (12,12,.1), floor)
    box('Backdrop wall', (0,.87,1.6), (8,.18,3.2), plaster)
    for i in range(4):
        box('Oak panel %d'%i, (-1.23+i*.615,.756,1.26), (.611,.05,2.52), oak, .0008)
    box('Shadow plinth', (0,.08,.05), (1.5,.58,.1), dark)
    box('Inset body', (0,.13,.42), (1.40,.60,.74), oak)
    box('Stone top 70mm', (0,0,.865), (1.84,.88,.07), stone, .0016)
    box('Stone end 70mm', (.885,0,.415), (.07,.88,.83), stone, .0010)
    # Separate sculptural metal sample, not a tap or a functional sink assembly.
    points = [(.28+.17*math.cos(math.pi*i/100), .15, 1.03+.17*math.sin(math.pi*i/100)) for i in range(101)]
    points = [(.45,.15,.9),(.45,.15,1.03)] + points + [(.11,.15,.9)]
    tube('Bronze arch sample', points, .016, bronze)
    # Authored fabric sample on the top; not a sofa throw or simulation claim.
    verts=[]; faces=[]; nu,nv=70,120
    for v in range(nv+1):
        t=v/nv
        for u in range(nu+1):
            q=u/nu; x=-.69+.54*q
            wave=.010*(1+math.sin(q*math.pi*5 + .5*math.sin(t*4)))
            y=.35-.61*t
            z=.902+wave*(.5+.5*math.sin(t*math.pi))
            verts.append((x,y,z))
            if u<nu and v<nv:
                a=v*(nu+1)+u; faces.append((a,a+1,a+nu+2,a+nu+1))
    mesh=bpy.data.meshes.new('Authored cloth'); mesh.from_pydata(verts,[],faces); mesh.update()
    obj=bpy.data.objects.new('Authored swatch, not simulated',mesh); bpy.context.collection.objects.link(obj)
    mesh.materials.append(cloth)
    for p in mesh.polygons:p.use_smooth=True
    mod=obj.modifiers.new('Thin textile', 'SOLIDIFY'); mod.thickness=.001
    # Window-like off-camera occluders shape the daylight; no copied architecture.
    box('Off-camera reveal',(-2.4,.1,1.5),(.18,2.2,3),plaster)
    box('Off-camera mullion',(-2.4,-1.7,1.5),(.10,.10,3),plaster)
    world=bpy.data.worlds.new('Soft cool sky'); world.use_nodes=True; sc.world=world
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.78,.87,1,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.25
    area('Broad side daylight',(-3,-2.5,3),(0,0,.8),600,3,(1,.92,.79))
    area('Cool room return',(1,-3,2),(0,.2,.8),60,2,(.85,.92,1))
    for name,loc,target,lens in [('Study hero',(2.65,-4.3,2.35),(0,.05,1.05),53),
                                  ('Study detail',(1.95,-2.5,1.6),(.33,-.03,.81),62)]:
        data=bpy.data.cameras.new(name); data.lens=lens
        cam=bpy.data.objects.new(name,data); bpy.context.collection.objects.link(cam)
        cam.location=loc;point_at(cam,target)
    sc.camera=bpy.data.objects['Study hero']
    bpy.context.view_layer.update()
    checks={'top_70mm':abs(bpy.data.objects['Stone top 70mm'].dimensions.z-.07)<1e-6,
            'end_70mm':abs(bpy.data.objects['Stone end 70mm'].dimensions.x-.07)<1e-6,
            'level_top':all(abs(a)<1e-8 for a in bpy.data.objects['Stone top 70mm'].rotation_euler),
            'two_cameras':len([o for o in sc.objects if o.type=='CAMERA'])==2,
            'no_external_images':not any(i.source=='FILE' for i in bpy.data.images)}
    if not all(checks.values()):raise RuntimeError(checks)
    bpy.ops.wm.save_as_mainfile(filepath=str(output/'study.blend'))
    bpy.ops.wm.open_mainfile(filepath=str(output/'study.blend'))
    # Verify the reopened source, not just the in-memory construction.
    if abs(bpy.data.objects['Stone top 70mm'].dimensions.z-.07)>1e-6:
        raise RuntimeError('Saved top thickness changed')
    (output/'study-checks.json').write_text(json.dumps({'scope':'Generic material fixture only',
         'checks':checks,'reopened':True,'production_quality_score':None},indent=2)+'\n')
    print('DEMO_SCENE_COMPLETE',flush=True)


if __name__=='__main__':main()

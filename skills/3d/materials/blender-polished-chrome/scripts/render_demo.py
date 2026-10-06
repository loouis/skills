"""Build/render original generic geometry in an isolated Blender process.

blender -b --factory-startup --python-exit-code 1 -P scripts/render_demo.py -- \
    --output /tmp/metal-demo-v01 --width 1600 --samples 256
"""
import argparse
import hashlib
import json
import math
import struct
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reflection_card import create_card


def material(name, color, roughness, metallic=0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Coat Weight'].default_value = 0
    return mat


def cylinder(name, radius, depth, location, mat, bevel):
    bpy.ops.mesh.primitive_cylinder_add(vertices=192, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    for face in obj.data.polygons:
        face.use_smooth = len(face.vertices) == 4
    mod = obj.modifiers.new('Manufactured edge', 'BEVEL')
    mod.width, mod.segments = bevel, 6
    return obj


def signature():
    scene = bpy.context.scene
    objects = {}
    for obj in scene.objects:
        if not obj.name.startswith('Study '):
            continue
        evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
        mesh = evaluated.to_mesh()
        record = {'matrix': [list(row) for row in obj.matrix_world],
                  'vertices': [list(v.co) for v in mesh.vertices],
                  'faces': [list(p.vertices) for p in mesh.polygons],
                  'normals': [list(n.vector) for n in mesh.corner_normals]}
        objects[obj.name] = hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest()
        evaluated.to_mesh_clear()
    camera = scene.camera
    return {'objects': objects, 'camera': [list(row) for row in camera.matrix_world],
            'ortho_scale': camera.data.ortho_scale, 'exposure': scene.view_settings.exposure,
            'transform': scene.view_settings.view_transform, 'look': scene.view_settings.look}


def configure_device(scene, device):
    scene.cycles.device = 'CPU'
    if device == 'CPU':
        return
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = device
    prefs.get_devices()
    available = [d for d in prefs.devices if d.type == device]
    if not available:
        raise RuntimeError(f'No Cycles {device} device found; use --device CPU')
    for item in prefs.devices:
        item.use = item.type == device
    scene.cycles.device = 'GPU'  # Session only; never save user preferences.


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--width', type=int, default=1600)
    parser.add_argument('--samples', type=int, default=256)
    parser.add_argument('--device', choices=['CPU', 'METAL', 'CUDA', 'OPTIX', 'HIP', 'ONEAPI'], default='CPU')
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
    if args.width < 320 or args.samples < 1:
        parser.error('Use width >= 320 and samples >= 1')
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)  # Never overwrite an earlier study.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    configure_device(scene, args.device)
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1
    scene.cycles.samples = args.samples
    scene.cycles.adaptive_threshold = .006
    scene.cycles.adaptive_min_samples = min(64, args.samples)
    scene.cycles.use_denoising = True
    scene.cycles.filter_width = 1
    scene.cycles.seed = 23
    scene.render.resolution_x = args.width
    scene.render.resolution_y = round(args.width * 3 / 4)
    scene.render.resolution_percentage = 100
    scene.render.use_motion_blur = False
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.image_settings.color_depth = '16'
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - High Contrast'
    scene.view_settings.exposure = 0

    world = bpy.data.worlds.new('Neutral studio')
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes['Background'].inputs[0].default_value = (.16, .17, .19, 1)
    world.node_tree.nodes['Background'].inputs[1].default_value = .5
    metal = material('Uncoated stainless approximation', (.56, .57, .58), .12, 1)
    floor_mat = material('Warm grey stage', (.3, .29, .27), .65)
    bpy.ops.mesh.primitive_plane_add(size=200)
    floor = bpy.context.object
    floor.name = 'Floor'
    floor.data.materials.append(floor_mat)
    cylinder('Study body', .075, .35, (-.115, .045, .179), metal, .007)
    cylinder('Study foot', .088, .018, (-.115, .045, .009), metal, .003)
    cylinder('Study crown', .069, .01, (-.115, .045, .358), metal, .002)
    bpy.ops.mesh.primitive_torus_add(major_segments=192, minor_segments=64, major_radius=.089,
                                   minor_radius=.027, location=(.23, .12, .116),
                                   rotation=(math.pi / 2, 0, math.radians(-14)))
    torus = bpy.context.object
    torus.name = 'Study ring'
    torus.data.materials.append(metal)
    for face in torus.data.polygons:
        face.use_smooth = True

    bpy.ops.object.camera_add(location=(.65, -1.5, .76))
    camera = bpy.context.object
    camera.name = 'Camera'
    camera.rotation_euler = (Vector((.04, .045, .172)) - camera.location).to_track_quat('-Z', 'Y').to_euler()
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = .76
    camera.data.dof.use_dof = False
    scene.camera = camera
    soft = ((0, 0), (.2, .8), (.45, 1), (.6, 1), (.85, .7), (1, 0))
    create_card('Left diffusion', size=(.7, 1.1), location=(-.6, -.4, .7), target=(0, 0, .18),
                strength=6, x_stops=soft, y_stops=soft,
                tone_stops=((0, .15), (.35, 1), (.7, .9), (1, .12)))
    create_card('Right diffusion', size=(.65, 1.2), location=(.65, .1, .7), target=(0, 0, .18),
                strength=4, grey=1, x_stops=soft, y_stops=soft)
    create_card('Overhead diffusion', size=(2.2, 3.4), location=(0, .6, 1.1), target=(0, .6, 0),
                strength=5, grey=1, x_stops=soft, y_stops=soft)
    card = create_card('Floor reflection', size=(.8, 1.6), location=(.1, -.8, .0008), target=(.1, -.8, 1))
    card.hide_render = True
    bpy.context.view_layer.update()
    baseline = signature()
    records = []
    variants = [('satin', .12, False), ('polish-only', .035, False), ('controlled', .035, True)]
    for name, roughness, controlled in variants:
        metal.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = roughness
        card.hide_render = not controlled
        # JPEG export can reset color_depth; explicitly restore it for every PNG.
        scene.render.image_settings.file_format = 'PNG'
        scene.render.image_settings.color_depth = '16'
        scene.render.filepath = f'//{name}.png'
        blend = output / f'{name}.blend'
        bpy.ops.wm.save_as_mainfile(filepath=str(blend))
        bpy.ops.render.render(write_still=True)
        png_header = (output / f'{name}.png').read_bytes()[:25]
        assert struct.unpack('>II', png_header[16:24]) == (args.width, round(args.width * 3 / 4))
        assert png_header[24] == 16, 'PNG master must retain 16-bit depth'
        scene.render.image_settings.file_format = 'JPEG'
        scene.render.image_settings.quality = 98
        bpy.data.images['Render Result'].save_render(str(output / f'{name}.jpg'), scene=scene)
        scene.render.image_settings.file_format = 'PNG'
        assert signature() == baseline, 'Study geometry/camera changed'
        records.append({'variant': name, 'roughness': roughness, 'floor_card': controlled})

    for record in records:
        bpy.ops.wm.open_mainfile(filepath=str(output / f"{record['variant']}.blend"))
        assert signature() == baseline, 'Saved study geometry/camera differs'
        bsdf = bpy.data.materials['Uncoated stainless approximation'].node_tree.nodes['Principled BSDF']
        assert math.isclose(bsdf.inputs['Roughness'].default_value, record['roughness'], abs_tol=1e-6)
        assert all(math.isclose(a, b, abs_tol=1e-6) for a, b in zip(bsdf.inputs['Base Color'].default_value, (.56, .57, .58, 1)))
        assert bsdf.inputs['Metallic'].default_value == 1 and bsdf.inputs['Coat Weight'].default_value == 0
        saved_card = bpy.data.objects['Floor reflection']
        assert saved_card.hide_render == (not record['floor_card'])
        assert not saved_card.visible_camera and not saved_card.visible_shadow and saved_card.visible_glossy
        assert bpy.data.objects['Floor'].visible_glossy
        assert bpy.context.scene.render.image_settings.color_depth == '16'
        record['saved_scene_verified'] = True
    report = {'blender': bpy.app.version_string, 'width': args.width, 'height': round(args.width * 3 / 4),
              'samples': args.samples, 'device': args.device, 'variants': records, 'invariants': baseline}
    (output / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: three actual renders, independent scenes and reopened preservation checks')


if __name__ == '__main__':
    main()

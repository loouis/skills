"""render_demo.py : a plain tiled pool seen under water, lit by the pool sunlight recipe.

    blender -b --factory-startup --python-exit-code 1 -P scripts/render_demo.py -- --output /path/to/new-folder

Makes the light map, builds the pool with pool_sunlight.py, renders it, and saves the image, a JPEG copy, the .blend and
a run.json into the output folder. The folder must be new and outside the skill. CPU unless --gpu is given.

    --draft            quarter-size map, 640 x 360, 64 samples: a setup check in about a minute, not a picture to judge
    --show floor|rays  leave out the sun rays, or the floor light, to see what each one adds
    --maps FILE        reuse maps already made (a <name>.json, or a loop's loop.json) instead of making them
    --frame N          with a loop's maps: which frame to render
    --subject          add a plain ball under water, with a ray-free zone around it and toward the sun
    --metres           build the same pool with one Blender unit = one metre (the picture must not change)
    --no-render        build and save the .blend only
    --scene FILE       another pool, camera, sun and recipe (default assets/demo-scene.json)
    --light FILE       another light map spec (default assets/demo-pool.json)

The scene file: pool {x, y, depth, rim} in mm, camera {location, pitch_down, lens, ray_clear [r0, r1]}, sun_travel,
floor_tiles, wall_tiles, sky, render, subject {location, radius, rgb, clear [r0, r1], clear_lift}, and recipe
{floor, rays, water, surface, sun, floor_sun, tiles}: any of pool_sunlight.RECIPE's numbers to replace.
camera.ray_clear thins the sun rays out around the lens (none inside r0, full from r1), because rays right in front
of the lens read as fog. subject.clear does the same around the ball, centred clear_lift mm from it toward the sun,
because a shaft between the sun and the ball takes light out and leaves a stain on it.
"""
import argparse
import json
import math
import os
import sys
import time

sys.dont_write_bytecode = True      # leave no __pycache__ in the skill folder
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
sys.path.insert(0, HERE)            # Blender's -P does not put the script's folder on the import path

import bpy                          # noqa: E402
import bmesh                        # noqa: E402
from mathutils import Vector        # noqa: E402

import make_light_map               # noqa: E402
import pool_sunlight as ps          # noqa: E402


def parse():
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    ap = argparse.ArgumentParser(prog='render_demo.py', description='Plain pool lit by the pool sunlight recipe.')
    ap.add_argument('--output', required=True, help='new folder, outside the skill')
    ap.add_argument('--scene', default=os.path.join(SKILL, 'assets', 'demo-scene.json'))
    ap.add_argument('--light', default=os.path.join(SKILL, 'assets', 'demo-pool.json'), help='light map spec')
    ap.add_argument('--maps', help='existing <name>.json or loop.json: use these maps and make none')
    ap.add_argument('--frame', type=int, default=1)
    ap.add_argument('--size', nargs=2, type=int, metavar=('W', 'H'))
    ap.add_argument('--samples', type=int)
    ap.add_argument('--seconds', type=float, default=0.0, help='stop the render after this long (0 = no limit)')
    ap.add_argument('--gpu', action='store_true')
    ap.add_argument('--draft', action='store_true')
    ap.add_argument('--show', choices=('both', 'floor', 'rays'), default='both')
    ap.add_argument('--subject', action='store_true')
    ap.add_argument('--metres', action='store_true')
    ap.add_argument('--no-render', action='store_true')
    return ap.parse_args(argv)


def fresh_folder(path):
    out = os.path.abspath(path)
    if os.path.commonpath([out, SKILL]) == SKILL:
        raise SystemExit('--output must be outside the skill folder')
    if os.path.exists(out) and os.listdir(out):
        raise SystemExit(f'{out} already has files in it: give a new folder')
    os.makedirs(out, exist_ok=True)
    return out


def mesh_object(name, verts, faces, material, collection, upm):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(c * upm for c in v) for v in verts], [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(material)
    collection.objects.link(ob)
    return ob


def box(name, x0, x1, y0, y1, z0, z1, material, collection, upm):
    v = [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    f = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    return mesh_object(name, v, f, material, collection, upm)


def build(a, cfg, light):
    upm = 0.001 if a.metres else 1.0
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    sc.unit_settings.scale_length = 1.0 if a.metres else 0.001
    coll = bpy.data.collections.new('Pool')
    sc.collection.children.link(coll)

    recipe = cfg.get('recipe', {})
    sun = cfg['sun_travel']
    (x0, x1), (y0, y1) = cfg['pool']['x'], cfg['pool']['y']
    zb, zt = -float(cfg['pool']['depth']), float(cfg['pool'].get('rim', 120))
    ft, wt = cfg['floor_tiles'], cfg['wall_tiles']

    # the floor and the walls under water
    if a.show == 'rays':
        floor_mat = ps.tile_material('Pool floor (plain)', 'XY', ft['a'], ft['b'], ft['grout'], upm, recipe.get('tiles'))
    else:
        floor_mat = ps.floor_light_material('Pool floor (sunlight map)', light, sun, ft['a'], ft['b'], ft['grout'], upm,
                                            0.0, recipe.get('floor'), recipe.get('tiles'))
    wall_xz = ps.tile_material('Pool wall (across)', 'XZ', wt['a'], wt['b'], wt['grout'], upm, recipe.get('tiles'))
    wall_yz = ps.tile_material('Pool wall (along)', 'YZ', wt['a'], wt['b'], wt['grout'], upm, recipe.get('tiles'))
    quad = [(0, 1, 2, 3)]
    floor = mesh_object('Pool floor', [(x0, y0, zb), (x1, y0, zb), (x1, y1, zb), (x0, y1, zb)], quad, floor_mat, coll, upm)
    walls = [
        mesh_object('Pool wall far', [(x0, y1, zb), (x1, y1, zb), (x1, y1, zt), (x0, y1, zt)], quad, wall_xz, coll, upm),
        mesh_object('Pool wall near', [(x1, y0, zb), (x0, y0, zb), (x0, y0, zt), (x1, y0, zt)], quad, wall_xz, coll, upm),
        mesh_object('Pool wall left', [(x0, y0, zb), (x0, y1, zb), (x0, y1, zt), (x0, y0, zt)], quad, wall_yz, coll, upm),
        mesh_object('Pool wall right', [(x1, y1, zb), (x1, y0, zb), (x1, y0, zt), (x1, y1, zt)], quad, wall_yz, coll, upm),
    ]

    # water: the surface, the body, and the layer that carries the sun rays
    mesh_object('Water surface', [(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)], quad,
                ps.water_surface_material('Water surface', recipe.get('surface')), coll, upm)
    # the body reaches a little past the floor and walls so none of its faces lies on a tiled face, and stops short of
    # the surface so a rippled surface never dips into it
    box('Water body', x0 - 30, x1 + 30, y0 - 30, y1 + 30, zb - 30, -14,
        ps.water_body_material('Water body', upm, recipe.get('water')), coll, upm)
    rays = ps.merged(ps.RECIPE['rays'], recipe.get('rays'))
    rays['clear'] = list(rays.get('clear', []))
    if cfg['camera'].get('ray_clear'):
        # rays right in front of the lens read as fog, not as rays: thin them out around the camera
        rays['clear'].append([*cfg['camera']['location'], *cfg['camera']['ray_clear'], [1, 1, 1]])
    if a.subject:
        s = cfg['subject']
        # the zone has to hold the water the sunlight crosses on its way to the subject, not only the subject:
        # clear_lift moves its centre that far toward the sharp sun, whose light is not bent at the surface
        centre = Vector(s['location']) - Vector(sun).normalized() * s.get('clear_lift', 0.0)
        rays['clear'].append([*centre, *s['clear'], [1, 1, 1]])
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=64, v_segments=32, radius=s['radius'] * upm)
        me = bpy.data.meshes.new('Ball')
        bm.to_mesh(me)
        bm.free()
        for p in me.polygons:
            p.use_smooth = True
        ball_mat = bpy.data.materials.new('Ball')
        ps.use_nodes(ball_mat)
        bsdf = ball_mat.node_tree.nodes['Principled BSDF']
        bsdf.inputs['Base Color'].default_value = (*s['rgb'], 1)
        bsdf.inputs['Roughness'].default_value = 0.45
        ball = bpy.data.objects.new('Ball', me)
        ball.data.materials.append(ball_mat)
        ball.location = Vector(s['location']) * upm
        coll.objects.link(ball)
    if a.show != 'floor':
        # 5 inside the body on every side: where two volumes share a face, rays skip one of them
        box('Sun rays (volume only)', x0 - 25, x1 + 25, y0 - 25, y1 + 25, -rays['depth'] - 40, -17,
            ps.sun_ray_material('Sun rays', light, sun, upm, 0.0, rays), coll, upm)

    ps.add_suns(coll, [floor] + walls, sun, recipe.get('sun'), recipe.get('floor_sun'))

    c = cfg['camera']
    cam_data = bpy.data.cameras.new('Pool camera')
    cam_data.lens = c['lens']
    cam_data.sensor_width = 36.0
    cam_data.clip_start = 5.0 * upm
    cam_data.clip_end = 60000.0 * upm
    cam = bpy.data.objects.new('Pool camera', cam_data)
    coll.objects.link(cam)
    cam.location = Vector(c['location']) * upm
    pitch = math.radians(c['pitch_down'])
    cam.rotation_mode = 'QUATERNION'
    cam.rotation_quaternion = Vector((0.0, math.cos(pitch), -math.sin(pitch))).to_track_quat('-Z', 'Y')
    sc.camera = cam

    r = dict(cfg['render'])
    if a.draft:
        r.update(size=[640, 360], samples=64)
    if a.size:
        r['size'] = a.size
    if a.samples:
        r['samples'] = a.samples
    device = ps.setup_render(sc, tuple(r['size']), r['samples'], r['adaptive'], a.seconds, a.gpu, r['exposure'],
                             r['white_balance'])
    sc.render.use_stamp_filename = False    # keep the .blend's path out of the saved images' metadata
    sky = cfg['sky']
    ps.setup_sky(sc, sky['horizon'], sky['zenith'], sky['strength'])
    sc.frame_set(a.frame)
    return sc, device, r


def main():
    a = parse()
    out = fresh_folder(a.output)
    with open(a.scene) as fh:
        cfg = json.load(fh)
    t0 = time.time()
    if a.maps:
        sidecar = os.path.abspath(a.maps)
    else:
        with open(a.light) as fh:
            spec = json.load(fh)
        if a.draft:
            spec['bins'] = int(spec.get('bins', 4096)) // 4
            spec['photons'] = int(spec.get('photons', 14336)) // 4
        print(f"making the light map ({spec['bins']} cells a side) ...", flush=True)
        make_light_map.make_still(spec, os.path.join(out, 'maps'))
        sidecar = os.path.join(out, 'maps', spec['name'] + '.json')
    t_map = time.time() - t0
    light = ps.load_light(sidecar)

    t1 = time.time()
    sc, device, r = build(a, cfg, light)
    blend = os.path.join(out, 'pool-sunlight.blend')
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    t_build = time.time() - t1

    run = {'blender': bpy.app.version_string, 'device': device, 'size': list(r['size']), 'samples': r['samples'],
           'show': a.show, 'draft': a.draft, 'subject': a.subject, 'units': 'metres' if a.metres else 'millimetres',
           'frame': a.frame, 'maps': os.path.relpath(sidecar, out) if not a.maps else sidecar,
           'seconds': {'map': round(t_map, 1), 'build': round(t_build, 1)}}
    if not a.no_render:
        png = os.path.join(out, 'pool-sunlight.png')
        sc.render.filepath = png
        t2 = time.time()
        bpy.ops.render.render(write_still=True)
        run['seconds']['render'] = round(time.time() - t2, 1)
        if not os.path.exists(png):
            raise SystemExit('the render ended without writing an image: run it again')
        sc.render.image_settings.file_format = 'JPEG'
        sc.render.image_settings.quality = 92
        bpy.data.images['Render Result'].save_render(os.path.join(out, 'pool-sunlight.jpg'), scene=sc)
        sc.render.image_settings.file_format = 'PNG'
    with open(os.path.join(out, 'run.json'), 'w') as fh:
        json.dump(run, fh, indent=1)
    print('RUN ' + json.dumps(run), flush=True)


if __name__ == '__main__':
    main()

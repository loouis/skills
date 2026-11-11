"""pool_sunlight.py : Blender (Cycles) builders for pool sunlight driven by a ray-density map.

Import this inside Blender and call the builders on your own scene, or run render_demo.py to see them on a plain pool.

    import sys; sys.path.insert(0, '<skill>/scripts'); import pool_sunlight as ps
    light = ps.load_light('<maps>/demo-pool.json')                       # made by make_light_map.py
    floor.data.materials.append(ps.floor_light_material('Pool floor', light, sun_travel, tile_a, tile_b, grout))
    ray_box.data.materials.append(ps.sun_ray_material('Sun rays', light, sun_travel))
    ps.add_suns(collection, [floor, wall], sun_travel)

Conventions
  Z is up and the water surface is the plane z = water_z.
  Every length in the recipe is in millimetres. `upm` is Blender units per millimetre: 1.0 when one unit is a
  millimetre, 0.001 when one unit is a metre. Positions are turned into millimetres at the top of each node tree, so
  the numbers in the recipe never change with the scene's unit; volume densities are per millimetre and are divided
  by `upm` when they are written into a node.
  `sun_travel` is the direction the sunlight travels (pointing down, away from the sun).
"""
import json
import math
import os

import bpy
from mathutils import Vector

N_WATER = 1.333

# The defaults below are the settings of the look this recipe was worked out on: a late-afternoon sun over a pool
# about 700 mm deep, seen at a low angle under water. Change them deliberately; references/recipe.md says what each does.
RECIPE = {
    'floor': {
        'sharp': 0.53, 'soft': 0.47,          # light = sharp map x 0.53 + soft map x 0.47
        'lo': 0.95, 'mul': 0.12,              # tile colour x (lo + mul x light) x wash
        'warm_gain': 3.8, 'warm_from': 1.0, 'warm_range': 10.0, 'warm_pow': 1.5, 'warm_rgb': [1.0, 0.86, 0.66],
        'fade': [1600.0, 4500.0, 0.35],       # from, to (mm from the camera), contrast kept at the far end
        'wash': {'base': 0.75, 'lobes': []},  # lobes: [cx, cy, sigma_x, sigma_y, gain] in lookup coordinates
    },
    'rays': {'density': 0.01, 'depth': 900.0, 'top': 25.0, 'falloff': 420.0, 'pow': 1.6, 'gain': 0.8,
             'rgb': [0.14, 0.88, 1.0], 'anisotropy': 0.0, 'clear': []},
    'water': {'absorb_rgb': [0.5, 0.83, 0.92], 'absorb_density': 0.0026,
              'scatter_rgb': [0.08, 0.85, 1.0], 'scatter_density': 0.00016, 'anisotropy': 0.0},
    'surface': {'ior': 1.333, 'roughness': 0.012, 'shadow_pass': 1.15},
    'sun': {'strength': 6.5, 'rgb': [1.0, 0.78, 0.55], 'angle': 0.6},
    'floor_sun': {'gain': 0.9, 'angle': 8.0, 'travel': None},
    'tiles': {'size': 90.0, 'grout': 1.6, 'bump': 0.2, 'rough': 0.18},
}


def merged(defaults, override):
    out = dict(defaults)
    for k, v in (override or {}).items():
        out[k] = merged(defaults[k], v) if isinstance(v, dict) and isinstance(defaults.get(k), dict) else v
    return out


# ---------------------------------------------------------------- small node helpers

def use_nodes(block):
    """Give a new material or world its node tree. Current Blender makes one from the start; older versions need the flag."""
    if block.node_tree is None:
        block.use_nodes = True


def _new_material(name):
    m = bpy.data.materials.new(name)
    use_nodes(m)
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    return m, nt, out


def _math(nt, op, *args):
    n = nt.nodes.new('ShaderNodeMath')
    n.operation = op
    for i, a in enumerate(args):
        if isinstance(a, (int, float)):
            n.inputs[i].default_value = a
        else:
            nt.links.new(a, n.inputs[i])
    return n.outputs[0]


def _map_range(nt, value, from_min, from_max, to_min, to_max, smooth=False):
    n = nt.nodes.new('ShaderNodeMapRange')
    if smooth:
        n.interpolation_type = 'SMOOTHSTEP'
    nt.links.new(value, n.inputs[0])
    for i, v in zip((1, 2, 3, 4), (from_min, from_max, to_min, to_max)):
        n.inputs[i].default_value = v
    return n.outputs[0]


def _mix_color(nt, blend, factor, a, b, clamp=True):
    """Mix node for colours. `factor`, `a`, `b` are sockets or values."""
    n = nt.nodes.new('ShaderNodeMix')
    n.data_type = 'RGBA'
    n.blend_type = blend
    n.clamp_factor = clamp
    n.clamp_result = False
    ins = {s.identifier: s for s in n.inputs}
    for key, val in (('Factor_Float', factor), ('A_Color', a), ('B_Color', b)):
        if isinstance(val, (int, float)):
            ins[key].default_value = val
        elif isinstance(val, (tuple, list)):
            ins[key].default_value = (*val[:3], 1.0)
        else:
            nt.links.new(val, ins[key])
    return {s.identifier: s for s in n.outputs}['Result_Color']


def _position_mm(nt, upm):
    """World position in millimetres, split into x, y, z sockets."""
    geo = nt.nodes.new('ShaderNodeNewGeometry')
    sc = nt.nodes.new('ShaderNodeVectorMath')
    sc.operation = 'SCALE'
    nt.links.new(geo.outputs['Position'], sc.inputs[0])
    sc.inputs['Scale'].default_value = 1.0 / upm
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(sc.outputs['Vector'], sep.inputs[0])
    return sc.outputs['Vector'], sep.outputs['X'], sep.outputs['Y'], sep.outputs['Z']


# ---------------------------------------------------------------- the light map

def load_light(sidecar_json):
    """Read what make_light_map.py wrote: `<name>.json` for a still, or `<name>/loop.json` for a loop."""
    with open(sidecar_json) as fh:
        info = json.load(fh)
    folder = os.path.dirname(os.path.abspath(sidecar_json))
    if 'frames' in info:
        return {'sharp': os.path.join(folder, 'sharp-0001.png'), 'soft': os.path.join(folder, 'soft-0001.png'),
                'scale': info['scale'], 'domain': info['domain'], 'frames': int(info['frames'])}
    return {'sharp': os.path.join(folder, info['files']['sharp']), 'soft': os.path.join(folder, info['files']['soft']),
            'scale': info['scale'], 'domain': info['domain'], 'frames': 0}


def _map_texture(nt, light, which, uv):
    tex = nt.nodes.new('ShaderNodeTexImage')
    img = bpy.data.images.load(light[which], check_existing=True)
    img.colorspace_settings.name = 'Non-Color'       # the map is data: no colour transform
    if light.get('frames'):
        img.source = 'SEQUENCE'
        iu = tex.image_user
        iu.frame_duration = light['frames']
        iu.frame_start = 1
        iu.frame_offset = 0
        iu.use_cyclic = True                         # frame N + 1 shows map 1 again
        iu.use_auto_refresh = True
    tex.image = img
    tex.extension = 'EXTEND'                         # never repeat the map: a repeat reads as wallpaper
    tex.interpolation = 'Cubic'
    nt.links.new(uv, tex.inputs['Vector'])
    return tex.outputs['Color']


def refracted_up(sun_travel):
    """Unit vector pointing up along the sun ray after it has entered the water (Snell's law at a flat surface)."""
    L = Vector(sun_travel).normalized()
    horiz = Vector((L.x, L.y, 0.0))
    sin_t = horiz.length / N_WATER
    cos_t = math.sqrt(1.0 - sin_t * sin_t)
    hd = horiz.normalized() * sin_t if horiz.length > 1e-9 else Vector((0.0, 0.0, 0.0))
    return Vector((-hd.x, -hd.y, cos_t))


def _lookup(nt, x, y, z, light, sun_travel, water_z):
    """Where a point's sunlight came in at the water surface, and the map coordinate for it.

    The map was made for a sun straight overhead. Sliding each point up the refracted sun ray to the surface puts the
    floor light and the sun rays on the same slanted lines, whatever the sun's direction."""
    up = refracted_up(sun_travel)
    t = _math(nt, 'MULTIPLY_ADD', z, -1.0 / up.z, water_z / up.z)          # (water_z - z) / up.z
    sx = _math(nt, 'MULTIPLY_ADD', t, up.x, x)
    sy = _math(nt, 'MULTIPLY_ADD', t, up.y, y)
    x0, y0, size = light['domain']
    uv = nt.nodes.new('ShaderNodeCombineXYZ')
    nt.links.new(_math(nt, 'MULTIPLY_ADD', sx, 1.0 / size, -x0 / size), uv.inputs['X'])
    nt.links.new(_math(nt, 'MULTIPLY_ADD', sy, 1.0 / size, -y0 / size), uv.inputs['Y'])
    return uv.outputs[0], sx, sy


# ---------------------------------------------------------------- materials

def _tiles(nt, x, y, colour_a, colour_b, grout_colour, t):
    """Square tiles on the plane (x, y) in millimetres. Returns the brick node."""
    vec = nt.nodes.new('ShaderNodeCombineXYZ')
    nt.links.new(x, vec.inputs['X'])
    nt.links.new(y, vec.inputs['Y'])
    br = nt.nodes.new('ShaderNodeTexBrick')
    br.offset = 0.0
    br.squash_frequency = 1
    br.offset_frequency = 1
    nt.links.new(vec.outputs[0], br.inputs['Vector'])
    br.inputs['Color1'].default_value = (*colour_a, 1)
    br.inputs['Color2'].default_value = (*colour_b, 1)
    br.inputs['Mortar'].default_value = (*grout_colour, 1)
    br.inputs['Scale'].default_value = 1.0
    br.inputs['Mortar Size'].default_value = t['grout']
    br.inputs['Mortar Smooth'].default_value = 0.35
    br.inputs['Bias'].default_value = 0.0
    br.inputs['Brick Width'].default_value = t['size']
    br.inputs['Row Height'].default_value = t['size']
    return br


def _finish_tiles(nt, out, br, base_colour, t, upm):
    bs = nt.nodes.new('ShaderNodeBsdfPrincipled')
    nt.links.new(base_colour, bs.inputs['Base Color'])
    nt.links.new(_map_range(nt, br.outputs['Fac'], 0.0, 1.0, t['rough'], 0.6), bs.inputs['Roughness'])
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = t['bump']
    bump.inputs['Distance'].default_value = 0.6 * upm
    nt.links.new(_math(nt, 'SUBTRACT', 1.0, br.outputs['Fac']), bump.inputs['Height'])
    nt.links.new(bump.outputs[0], bs.inputs['Normal'])
    nt.links.new(bs.outputs[0], out.inputs['Surface'])


def tile_material(name, plane, colour_a, colour_b, grout_colour, upm=1.0, tiles=None):
    """Plain tiles with no light pattern, for the walls. `plane` is the pair of axes the tiles lie on, e.g. 'XZ'."""
    t = merged(RECIPE['tiles'], tiles)
    m, nt, out = _new_material(name)
    _, x, y, z = _position_mm(nt, upm)
    ax = {'X': x, 'Y': y, 'Z': z}
    br = _tiles(nt, ax[plane[0]], ax[plane[1]], colour_a, colour_b, grout_colour, t)
    _finish_tiles(nt, out, br, br.outputs['Color'], t, upm)
    return m


def floor_light_material(name, light, sun_travel, colour_a, colour_b, grout_colour, upm=1.0, water_z=0.0,
                         floor=None, tiles=None):
    """Tiled pool floor carrying the sunlight map.

    light L   = sharp x 0.53 + soft x 0.47, then pulled toward 1 with distance from the camera
    wash W    = base + sum of broad Gaussians (where the sunlight lands; reads at thumbnail size)
    colour    = tile x (lo + mul x L) x W   +   warm x gain x clamp((L - from) / range) ^ pow x W
    Every step is continuous. There is no threshold anywhere, so no hard edge can appear."""
    f = merged(RECIPE['floor'], floor)
    t = merged(RECIPE['tiles'], tiles)
    m, nt, out = _new_material(name)
    _, x, y, z = _position_mm(nt, upm)
    br = _tiles(nt, x, y, colour_a, colour_b, grout_colour, t)
    uv, sx, sy = _lookup(nt, x, y, z, light, sun_travel, water_z)

    sharp = _math(nt, 'MULTIPLY', _map_texture(nt, light, 'sharp', uv), light['scale'] * f['sharp'])
    soft = _math(nt, 'MULTIPLY', _map_texture(nt, light, 'soft', uv), light['scale'] * f['soft'])
    L = _math(nt, 'ADD', sharp, soft)

    if f.get('fade'):
        # further away the pattern is seen through more water: its contrast eases back toward even light
        cam = nt.nodes.new('ShaderNodeCameraData')
        dist = _math(nt, 'MULTIPLY', cam.outputs['View Distance'], 1.0 / upm)
        keep = _map_range(nt, dist, f['fade'][0], f['fade'][1], 1.0, f['fade'][2], smooth=True)
        L = _math(nt, 'MULTIPLY_ADD', _math(nt, 'SUBTRACT', L, 1.0), keep, 1.0)

    wash = None
    for (cx, cy, sgx, sgy, gain) in f['wash'].get('lobes', []):
        dx = _math(nt, 'SUBTRACT', sx, cx)
        dy = _math(nt, 'SUBTRACT', sy, cy)
        ex = _math(nt, 'MULTIPLY', _math(nt, 'MULTIPLY', dx, dx), -1.0 / (2 * sgx * sgx))
        ey = _math(nt, 'MULTIPLY_ADD', _math(nt, 'MULTIPLY', dy, dy), -1.0 / (2 * sgy * sgy), ex)
        lobe = _math(nt, 'MULTIPLY', _math(nt, 'EXPONENT', ey), gain)
        wash = _math(nt, 'ADD', lobe, f['wash'].get('base', 1.0) if wash is None else wash)

    grey = _math(nt, 'MULTIPLY_ADD', L, f['mul'], f['lo'])
    if wash is not None:
        grey = _math(nt, 'MULTIPLY', grey, wash)
    grey_rgb = nt.nodes.new('ShaderNodeCombineColor')
    for ch in ('Red', 'Green', 'Blue'):
        nt.links.new(grey, grey_rgb.inputs[ch])
    lit = _mix_color(nt, 'MULTIPLY', 1.0, br.outputs['Color'], grey_rgb.outputs[0])

    warm = _map_range(nt, L, f['warm_from'], f['warm_from'] + f['warm_range'], 0.0, 1.0)
    warm = _math(nt, 'MULTIPLY', _math(nt, 'POWER', warm, f['warm_pow']), f['warm_gain'])
    if wash is not None:
        warm = _math(nt, 'MULTIPLY', warm, wash)
    # the factor is left unclamped: the tightest gathering has to climb past a pale tint to a warm-white centre
    colour = _mix_color(nt, 'ADD', warm, lit, f['warm_rgb'], clamp=False)
    _finish_tiles(nt, out, br, colour, t, upm)
    return m


def water_surface_material(name, surface=None):
    """Glass to the eye, a flat pass to shadow rays.

    Camera and bounce rays see refraction and reflection. Shadow rays (the sunlight on its way down) pass straight
    through at a fixed gain, so the surface's own ripples cannot print a second, competing pattern on the floor."""
    s = merged(RECIPE['surface'], surface)
    m, nt, out = _new_material(name)
    glass = nt.nodes.new('ShaderNodeBsdfGlass')
    glass.distribution = 'GGX'
    glass.inputs['IOR'].default_value = s['ior']
    glass.inputs['Roughness'].default_value = s['roughness']
    clear = nt.nodes.new('ShaderNodeBsdfTransparent')
    p = s['shadow_pass']
    clear.inputs['Color'].default_value = (p, p, p, 1)
    lp = nt.nodes.new('ShaderNodeLightPath')
    mix = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(lp.outputs['Is Shadow Ray'], mix.inputs[0])
    nt.links.new(glass.outputs[0], mix.inputs[1])
    nt.links.new(clear.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs['Surface'])
    return m


def water_body_material(name, upm=1.0, water=None):
    """The water itself: absorption for the blue-green depth colour, a little even scatter for the haze."""
    w = merged(RECIPE['water'], water)
    m, nt, out = _new_material(name)
    va = nt.nodes.new('ShaderNodeVolumeAbsorption')
    va.inputs['Color'].default_value = (*w['absorb_rgb'], 1)
    va.inputs['Density'].default_value = w['absorb_density'] / upm
    vs = nt.nodes.new('ShaderNodeVolumeScatter')
    vs.inputs['Color'].default_value = (*w['scatter_rgb'], 1)
    vs.inputs['Density'].default_value = w['scatter_density'] / upm
    vs.inputs['Anisotropy'].default_value = w['anisotropy']
    add = nt.nodes.new('ShaderNodeAddShader')
    nt.links.new(va.outputs[0], add.inputs[0])
    nt.links.new(vs.outputs[0], add.inputs[1])
    nt.links.new(add.outputs[0], out.inputs['Volume'])
    return m


def sun_ray_material(name, light, sun_travel, upm=1.0, water_z=0.0, rays=None):
    """Sun rays in the water, read from the same map as the floor light.

    density = depth fade x max(soft map - 1, 0) ^ pow x gain
    A point in the water looks the soft map up where its sun ray entered the surface, exactly as the floor does, so
    every shaft stands on a bright part of the floor and the two never drift apart."""
    r = merged(RECIPE['rays'], rays)
    m, nt, out = _new_material(name)
    pos, x, y, z = _position_mm(nt, upm)
    uv, _, _ = _lookup(nt, x, y, z, light, sun_travel, water_z)
    soft = _map_texture(nt, light, 'soft', uv)
    over = _math(nt, 'MAXIMUM', _math(nt, 'MULTIPLY_ADD', soft, light['scale'], -1.0), 0.0)
    power = _math(nt, 'POWER', over, r['pow'])
    # strongest just under the surface, gone by `depth`; the exponential thins them faster on the way down
    fade = _map_range(nt, z, water_z - r['depth'], water_z - r['top'], 0.0, r['density'] / upm, smooth=True)
    fade = _math(nt, 'MULTIPLY', fade, _math(nt, 'EXPONENT', _math(nt, 'MULTIPLY_ADD', z, 1.0 / r['falloff'], -water_z / r['falloff'])))
    dens = _math(nt, 'MULTIPLY', _math(nt, 'MULTIPLY', fade, power), r['gain'])
    for (cx, cy, cz, r0, r1, squash) in r.get('clear', []):
        # keep a subject's body free of rays: no density inside r0, full density beyond r1
        d = nt.nodes.new('ShaderNodeVectorMath')
        d.operation = 'SUBTRACT'
        nt.links.new(pos, d.inputs[0])
        d.inputs[1].default_value = (cx, cy, cz)
        sq = nt.nodes.new('ShaderNodeVectorMath')
        sq.operation = 'MULTIPLY'
        nt.links.new(d.outputs[0], sq.inputs[0])
        sq.inputs[1].default_value = tuple(squash)
        ln = nt.nodes.new('ShaderNodeVectorMath')
        ln.operation = 'LENGTH'
        nt.links.new(sq.outputs[0], ln.inputs[0])
        dens = _math(nt, 'MULTIPLY', dens, _map_range(nt, ln.outputs['Value'], r0, r1, 0.0, 1.0, smooth=True))
    vs = nt.nodes.new('ShaderNodeVolumeScatter')
    vs.inputs['Color'].default_value = (*r['rgb'], 1)
    vs.inputs['Anisotropy'].default_value = r['anisotropy']
    nt.links.new(dens, vs.inputs['Density'])
    nt.links.new(vs.outputs[0], out.inputs['Volume'])
    return m


# ---------------------------------------------------------------- lights

def add_suns(collection, floor_and_walls, sun_travel, sun=None, floor_sun=None, name='Pool'):
    """Two suns, split with light linking.

    The sharp sun lights everything except the floor and the underwater walls. Those are lit by a second, wide sun
    alone, so nothing above them (a ripple, a subject's edge) can draw a crisp shape on the tiles to fight the map.
    Do not also give the wide sun a shadow-linking collection: in Cycles 5.2 that left the floor dark and speckled."""
    s = merged(RECIPE['sun'], sun)
    fs = merged(RECIPE['floor_sun'], floor_sun)
    direction = Vector(sun_travel).normalized()

    main_data = bpy.data.lights.new(f'{name} sun', 'SUN')
    main_data.energy = s['strength']
    main_data.color = tuple(s['rgb'])
    main_data.angle = math.radians(s['angle'])
    main = bpy.data.objects.new(f'{name} sun', main_data)
    collection.objects.link(main)
    main.rotation_mode = 'QUATERNION'
    main.rotation_quaternion = direction.to_track_quat('-Z', 'Y')

    not_these = bpy.data.collections.new(f'{name} sharp sun leaves out')
    only_these = bpy.data.collections.new(f'{name} wide sun lights only')
    for ob in floor_and_walls:
        not_these.objects.link(ob)
        only_these.objects.link(ob)
    for co in not_these.collection_objects:
        co.light_linking.link_state = 'EXCLUDE'
    for co in only_these.collection_objects:
        co.light_linking.link_state = 'INCLUDE'
    main.light_linking.receiver_collection = not_these

    # by default the wide sun comes down the refracted sun direction, which is where sunlight under water travels
    travel = Vector(fs['travel']).normalized() if fs.get('travel') else -refracted_up(sun_travel)
    wide_data = bpy.data.lights.new(f'{name} floor sun (wide)', 'SUN')
    wide_data.energy = s['strength'] * fs['gain']
    wide_data.color = tuple(s['rgb'])
    wide_data.angle = math.radians(fs['angle'])
    wide = bpy.data.objects.new(f'{name} floor sun (wide)', wide_data)
    collection.objects.link(wide)
    wide.rotation_mode = 'QUATERNION'
    wide.rotation_quaternion = travel.to_track_quat('-Z', 'Y')
    wide.light_linking.receiver_collection = only_these
    return main, wide


# ---------------------------------------------------------------- render settings

def setup_render(scene, size=(1280, 720), samples=320, adaptive=0.03, seconds=0.0, gpu=False, exposure=0.05,
                 white_balance=7800.0):
    scene.render.engine = 'CYCLES'
    c = scene.cycles
    c.device = 'CPU'
    if gpu:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        for kind in ('METAL', 'OPTIX', 'CUDA', 'HIP', 'ONEAPI'):
            try:
                prefs.compute_device_type = kind
            except TypeError:
                continue
            prefs.get_devices()
            found = [d for d in prefs.devices if d.type == kind]
            if found:
                for d in prefs.devices:
                    d.use = d.type == kind
                c.device = 'GPU'
                break
    c.samples = samples
    c.use_adaptive_sampling = True
    c.adaptive_threshold = adaptive
    c.time_limit = seconds
    c.use_denoising = True
    c.denoiser = 'OPENIMAGEDENOISE'
    c.max_bounces = 16
    c.diffuse_bounces = 3
    c.glossy_bounces = 6
    c.transmission_bounces = 12
    c.volume_bounces = 1
    c.transparent_max_bounces = 64
    c.caustics_reflective = False
    c.caustics_refractive = False        # the pattern comes from the map, never from path-traced caustics
    c.blur_glossy = 1.0
    c.sample_clamp_indirect = 8.0
    c.use_light_tree = False             # with the light tree on, the two linked suns sampled unevenly
    scene.render.resolution_x, scene.render.resolution_y = size
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    scene.render.filter_size = 1.2
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.image_settings.color_depth = '8'
    vs = scene.view_settings
    vs.view_transform = 'AgX'
    vs.look = 'AgX - Medium High Contrast'
    vs.exposure = exposure
    if white_balance and hasattr(vs, 'use_white_balance'):
        vs.use_white_balance = True
        vs.white_balance_temperature = white_balance
        vs.white_balance_tint = 0.0
    return c.device


def setup_sky(scene, horizon=(0.55, 0.7, 0.92), zenith=(0.24, 0.42, 0.8), strength=0.42):
    world = bpy.data.worlds.new('Pool sky')
    use_nodes(world)
    nt = world.node_tree
    bg = nt.nodes['Background']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (*horizon, 1)
    ramp.color_ramp.elements[1].position = 0.6
    ramp.color_ramp.elements[1].color = (*zenith, 1)
    nt.links.new(tc.outputs['Generated'], sep.inputs[0])
    nt.links.new(sep.outputs['Z'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = strength
    scene.world = world
    return world

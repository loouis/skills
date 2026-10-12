"""Portable native splash helpers. Run with Blender; never overwrite an input/job."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def recipe():
    return json.loads((ROOT / 'assets/recipe.json').read_text())


def fresh_output(value):
    path = Path(value).expanduser().resolve()
    if path == ROOT or ROOT in path.parents:
        raise ValueError('Write generated work outside the skill')
    path.mkdir(parents=True, exist_ok=False)
    return path


def water_material():
    material = bpy.data.materials.new('Neutral water in air')
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    glass = nodes.new('ShaderNodeBsdfGlass')
    glass.distribution = 'BECKMANN'
    glass.inputs['Color'].default_value = (1, 1, 1, 1)
    glass.inputs['IOR'].default_value = 1.333
    glass.inputs['Roughness'].default_value = 0
    output = nodes.new('ShaderNodeOutputMaterial')
    material.node_tree.links.new(glass.outputs[0], output.inputs['Surface'])
    return material


def weights(world_coordinates, field):
    x, _, z = np.asarray(world_coordinates).T
    def smooth(value):
        value = np.clip(value, 0, 1)
        return value * value * (3 - 2 * value)
    return (smooth((field['x_outer'] - np.abs(x)) / field['x_fade']) *
            smooth((z - field['z_low']) / field['z_low_fade']) *
            smooth((field['z_high'] - z) / field['z_high_fade']))


def configure(output, settings):
    scene = bpy.context.scene
    original = [o for o in scene.objects if o.type == 'MESH' and o.get('splash_source')]
    if not original:
        raise ValueError('Tag closed mesh sources with splash_source = true')
    if any(o.modifiers.get('Splash initial volume') for o in original):
        raise ValueError('Sources are already configured')
    source = settings['source']
    for obj in original:
        if obj.get('splash_role', 'sheet') not in source['velocity']:
            raise ValueError('splash_role must be sheet, plume or trail')
    depsgraph = bpy.context.evaluated_depsgraph_get()
    sources = []
    for obj in original:
        data = bpy.data.meshes.new_from_object(obj.evaluated_get(depsgraph), depsgraph=depsgraph)
        current = bpy.data.objects.new('Source | ' + obj.name, data)
        scene.collection.objects.link(current)
        current.matrix_world = obj.matrix_world.copy()
        role = obj.get('splash_role', 'sheet')
        current['splash_source'] = True
        current['splash_role'] = role
        modifier = current.modifiers.new('Splash initial volume', 'FLUID')
        modifier.fluid_type = 'FLOW'
        flow = modifier.flow_settings
        flow.flow_type, flow.flow_behavior = 'LIQUID', 'GEOMETRY'
        flow.use_initial_velocity = True
        flow.surface_distance = source['expansion_voxels']
        flow.velocity_coord = source['velocity'][role]
        current.hide_render = True
        sources.append(current.name)
    for obj in original:
        bpy.data.objects.remove(obj, do_unlink=True)
    cfg = settings['domain']
    scene.frame_start, scene.frame_end = cfg['frames']
    scene.render.fps = cfg['fps']
    scene.gravity = cfg['gravity']
    bpy.ops.mesh.primitive_cube_add(size=1, location=cfg['location'])
    obj = bpy.context.object
    obj.name = 'Splash domain'
    obj.dimensions = cfg['dimensions']
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    modifier = obj.modifiers.new('Splash FLIP', 'FLUID')
    modifier.fluid_type = 'DOMAIN'
    domain = modifier.domain_settings
    domain.domain_type = 'LIQUID'
    domain.resolution_max = cfg['resolution']
    domain.cache_type = 'ALL'
    domain.cache_directory = str(output / 'cache')
    domain.cache_frame_start, domain.cache_frame_end = cfg['frames']
    domain.cache_mesh_format = 'BOBJECT'
    domain.cache_data_format = domain.cache_particle_format = 'UNI'
    domain.use_mesh = True
    domain.mesh_scale = cfg['mesh_scale']
    domain.mesh_particle_radius = cfg['mesh_radius']
    domain.mesh_smoothen_pos, domain.mesh_smoothen_neg = cfg['mesh_smoothing']
    domain.mesh_generator = 'IMPROVED'
    domain.flip_ratio = cfg['flip_ratio']
    domain.particle_randomness = cfg['randomness']
    domain.time_scale = cfg['time_scale']
    domain.timesteps_min, domain.timesteps_max = cfg['timesteps']
    domain.cfl_condition = cfg['cfl']
    domain.use_fractions = False
    domain.use_diffusion = cfg['diffusion']
    domain.surface_tension = cfg['surface_tension_field']
    for direction in ['front', 'back', 'left', 'right', 'top', 'bottom']:
        setattr(domain, 'use_collision_border_' + direction, False)
    obj.data.materials.append(water_material())
    return {'domain': obj.name, 'sources': sources, 'baked': False}


def freeze(name, frame):
    scene = bpy.context.scene
    obj = scene.objects.get(name)
    if obj is None:
        raise ValueError('Domain object not found')
    modifiers = [m for m in obj.modifiers if m.type == 'FLUID' and m.fluid_type == 'DOMAIN']
    if len(modifiers) != 1 or not modifiers[0].domain_settings.has_cache_baked_mesh:
        raise ValueError('Freeze requires a completed liquid mesh cache')
    domain = modifiers[0].domain_settings
    if not domain.cache_frame_start <= frame <= domain.cache_frame_end:
        raise ValueError('Frame lies outside the baked range')
    scene.frame_set(frame)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    data = bpy.data.meshes.new_from_object(obj.evaluated_get(depsgraph), depsgraph=depsgraph)
    if len(data.vertices) < 24:
        raise ValueError('No usable resolved liquid surface at this frame')
    result = bpy.data.objects.new('Frozen splash', data)
    scene.collection.objects.link(result)
    result.matrix_world = obj.matrix_world.copy()
    result['splash_method'] = 'Frozen native frame; not validated animation'
    for polygon in data.polygons:
        polygon.use_smooth = True
    bpy.data.objects.remove(obj, do_unlink=True)
    for source in list(scene.objects):
        if source.get('splash_source'):
            bpy.data.objects.remove(source, do_unlink=True)
    return result


def refine(obj, cfg):
    if obj.type != 'MESH' or any(m.type not in {'SUBSURF', 'SMOOTH'} for m in obj.modifiers):
        raise ValueError('Refine a frozen mesh with only Smooth/Subdivision modifiers')
    if obj.vertex_groups:
        raise ValueError('Use a copy without pre-existing vertex groups')
    if obj.data.users > 1:
        obj.data = obj.data.copy()
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    had_smoothing = any(m.type == 'SMOOTH' for m in obj.modifiers)
    for modifier in list(obj.modifiers):
        if modifier.type == 'SUBSURF':
            obj.modifiers.remove(modifier)
        else:
            bpy.ops.object.modifier_apply(modifier=modifier.name)
    if not had_smoothing and cfg['base_factor'] and cfg['base_iterations']:
        base = obj.modifiers.new('Native base smoothing', 'SMOOTH')
        base.factor, base.iterations = cfg['base_factor'], cfg['base_iterations']
        bpy.ops.object.modifier_apply(modifier=base.name)
    count = len(obj.data.vertices)
    coords = np.empty(count * 3, np.float32)
    obj.data.vertices.foreach_get('co', coords)
    matrix = np.array(obj.matrix_world)
    coords = coords.reshape(-1, 3)
    world = coords @ matrix[:3, :3].T + matrix[:3, 3]
    field = weights(world, cfg['field'])
    group = obj.vertex_groups.new(name='Bounded membrane field')
    levels = np.rint(field * cfg['quantization']).astype(int)
    for level in np.unique(levels):
        if level:
            group.add(np.flatnonzero(levels == level).tolist(), float(level) / cfg['quantization'], 'REPLACE')
    if cfg['factor'] and cfg['iterations'] and np.any(levels):
        modifier = obj.modifiers.new('Bounded membrane smoothing', 'SMOOTH')
        modifier.vertex_group = group.name
        modifier.factor, modifier.iterations = cfg['factor'], cfg['iterations']
        bpy.ops.object.modifier_apply(modifier=modifier.name)
    coords = np.empty(count * 3, np.float32)
    normals = np.empty(count * 3, np.float32)
    obj.data.vertices.foreach_get('co', coords)
    obj.data.vertices.foreach_get('normal', normals)
    normal_matrix = np.linalg.inv(matrix[:3, :3]).T
    normals = normals.reshape(-1, 3) @ normal_matrix.T
    normals /= np.maximum(np.linalg.norm(normals, axis=1)[:, None], 1e-12)
    delta = normals * (cfg['outward_offset'] * field[:, None])
    local_delta = delta @ np.linalg.inv(matrix[:3, :3]).T
    updated = coords.reshape(-1, 3) + local_delta
    obj.data.vertices.foreach_set('co', updated.astype(np.float32).ravel())
    obj.data.update()
    obj.vertex_groups.clear()
    if cfg['subdivision']:
        modifier = obj.modifiers.new('Final subdivision', 'SUBSURF')
        modifier.levels = modifier.render_levels = cfg['subdivision']
    return {'vertices': count, 'weighted_vertices': int(np.count_nonzero(field)), 'filter': cfg}


def save(output, record):
    scene = bpy.context.scene
    scene.render.filepath = str(output / 'beauty.png')
    tree = getattr(scene, 'compositing_node_group', None)
    if tree:
        for node in tree.nodes:
            if node.type == 'OUTPUT_FILE':
                node.directory = str(output)
    scene['splash_scope'] = 'Still workflow; validate new motion separately'
    bpy.ops.wm.save_as_mainfile(filepath=str(output / 'scene.blend'), compress=True)
    record['blender'] = bpy.app.version_string
    record['scene_sha256'] = hashlib.sha256((output / 'scene.blend').read_bytes()).hexdigest()
    (output / 'record.json').write_text(json.dumps(record, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['configure', 'freeze', 'refine'])
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--recipe', type=Path, default=ROOT / 'assets/recipe.json')
    parser.add_argument('--domain', default='Splash domain')
    parser.add_argument('--object', default='Frozen splash')
    parser.add_argument('--frame', type=int, default=9)
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
    source = args.input.expanduser().resolve(strict=True)
    settings = json.loads(args.recipe.read_text())
    output = fresh_output(args.output)
    bpy.ops.wm.open_mainfile(filepath=str(source))
    if args.action == 'configure':
        result = configure(output, settings)
    elif args.action == 'freeze':
        obj = freeze(args.domain, args.frame)
        result = {'object': obj.name, 'vertices': len(obj.data.vertices), 'frame': args.frame}
    else:
        obj = bpy.context.scene.objects.get(args.object)
        if obj is None:
            raise ValueError('Frozen mesh not found')
        result = refine(obj, settings['filter'])
    save(output, {'action': args.action, 'settings': settings, 'result': result,
                  'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest()})


if __name__ == '__main__':
    main()

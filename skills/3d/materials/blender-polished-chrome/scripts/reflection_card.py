"""Optional Blender helper: add a feathered reflection card, leaving the scene intact."""
import math

import bpy
from mathutils import Quaternion, Vector


X_STOPS = ((0, 0), (.25, .85), (.7, .85), (1, 0))
Y_STOPS = ((0, 0), (.1, 1), (.9, 1), (1, 0))


def _stops(values, label):
    values = tuple(tuple(float(v) for v in pair) for pair in values)
    if len(values) < 2 or len(values) > 32 or any(len(p) != 2 for p in values):
        raise ValueError(f"{label}: provide 2–32 (position, value) pairs")
    if any(not math.isfinite(v) or not 0 <= v <= 1 for p in values for v in p):
        raise ValueError(f"{label}: positions and values must be finite and in [0, 1]")
    if values[0][0] != 0 or values[-1][0] != 1:
        raise ValueError(f"{label}: positions must span 0 to 1")
    if any(a[0] >= b[0] for a, b in zip(values, values[1:])):
        raise ValueError(f"{label}: positions must be strictly increasing")
    return values


def _vector(values, length, label):
    result = tuple(float(v) for v in values)
    if len(result) != length or not all(math.isfinite(v) for v in result):
        raise ValueError(f"{label}: expected {length} finite coordinates")
    return result


def _ramp(tree, name, stops, source, location):
    node = tree.nodes.new('ShaderNodeValToRGB')
    node.name = node.label = name
    node.location = location
    ramp = node.color_ramp
    ramp.interpolation = 'B_SPLINE'
    # Set endpoints before inserting intermediate elements (the collection sorts).
    for element, (position, value) in zip(ramp.elements, (stops[0], stops[-1])):
        element.position = position
        element.color = (value, value, value, 1)
    for position, value in stops[1:-1]:
        element = ramp.elements.new(position)
        element.color = (value, value, value, 1)
    tree.links.new(source, node.inputs['Fac'])
    return node


def create_card(name, *, size, location, target, roll=0, grey=.012, strength=1,
                x_stops=X_STOPS, y_stops=Y_STOPS, tone_stops=None, collection=None):
    """Create a plane with explicit UVs; local +Z faces target, roll is radians.

    size is (width, height) in scene units. grey and ramp tones are linear RGB.
    Hidden from camera/direct shadow, visible to glossy and diffuse rays.
    Adds data only; never changes selection, existing objects or preferences.
    A supplied collection must already belong to the intended scene.
    """
    size = _vector(size, 2, 'size')
    location = _vector(location, 3, 'location')
    target = _vector(target, 3, 'target')
    direction = Vector(target) - Vector(location)
    if min(size) <= 0 or direction.length < 1e-10:
        raise ValueError('Size must be positive and target must differ from location')
    if not all(math.isfinite(v) for v in (roll, grey, strength)) or not 0 <= grey <= 1 or strength < 0:
        raise ValueError('Use finite roll, linear grey in [0, 1], and nonnegative strength')
    xs, ys = _stops(x_stops, 'x_stops'), _stops(y_stops, 'y_stops')
    tones = _stops(tone_stops, 'tone_stops') if tone_stops is not None else None

    mesh = bpy.data.meshes.new(name + ' mesh')
    w, h = size[0] / 2, size[1] / 2
    mesh.from_pydata([(-w, -h, 0), (w, -h, 0), (w, h, 0), (-w, h, 0)], [], [(0, 1, 2, 3)])
    mesh.update()
    uv = mesh.uv_layers.new(name='Card UV')
    for loop, coordinate in zip(mesh.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
        uv.data[loop.index].uv = coordinate
    obj = bpy.data.objects.new(name, mesh)
    (collection if collection is not None else bpy.context.scene.collection).objects.link(obj)
    obj.location = location
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = direction.to_track_quat('Z', 'Y') @ Quaternion((0, 0, 1), roll)
    obj.visible_camera = False
    obj.visible_shadow = False
    obj.visible_glossy = True
    obj.visible_diffuse = True

    material = bpy.data.materials.new(name + ' material')
    material.use_nodes = True
    tree = material.node_tree
    tree.nodes.clear()
    tc = tree.nodes.new('ShaderNodeTexCoord'); tc.location = (-850, 100)
    axes = tree.nodes.new('ShaderNodeSeparateXYZ'); axes.location = (-660, 100)
    tree.links.new(tc.outputs['UV'], axes.inputs[0])
    xr = _ramp(tree, 'X feather', xs, axes.outputs['X'], (-450, 250))
    yr = _ramp(tree, 'Y feather', ys, axes.outputs['Y'], (-450, -30))
    product = tree.nodes.new('ShaderNodeMath'); product.operation = 'MULTIPLY'; product.location = (-120, 180)
    tree.links.new(xr.outputs['Color'], product.inputs[0])
    tree.links.new(yr.outputs['Color'], product.inputs[1])
    emission = tree.nodes.new('ShaderNodeEmission'); emission.location = (-100, -220)
    emission.inputs['Color'].default_value = (grey, grey, grey, 1)
    emission.inputs['Strength'].default_value = strength
    if tones is not None:
        tone = _ramp(tree, 'X tone', tones, axes.outputs['X'], (-450, -310))
        tree.links.new(tone.outputs['Color'], emission.inputs['Color'])
    transparent = tree.nodes.new('ShaderNodeBsdfTransparent'); transparent.location = (-100, -50)
    mix = tree.nodes.new('ShaderNodeMixShader'); mix.location = (150, 150)
    tree.links.new(product.outputs[0], mix.inputs[0])
    tree.links.new(transparent.outputs[0], mix.inputs[1])
    tree.links.new(emission.outputs[0], mix.inputs[2])
    out = tree.nodes.new('ShaderNodeOutputMaterial'); out.location = (360, 150)
    tree.links.new(mix.outputs[0], out.inputs['Surface'])
    mesh.materials.append(material)
    return obj
